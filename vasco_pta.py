from pta_helper import *
import copy
<<<<<<< HEAD
import json
import os

# --- NEW HELPER FOR JSON EXPORT ---
def save_vasco_json(ptr_dict: PointerDict, filepath: str):
    """Safely serializes the pointer dictionary (converting sets to lists) and writes to JSON."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    serializable_dict = {}
    for var, fld_dict in ptr_dict.items():
        serializable_dict[var] = {}
        for fld, pts in fld_dict.items():
            serializable_dict[var][fld] = list(pts)
    with open(filepath, 'w') as f:
        json.dump(serializable_dict, f, indent=4)
# ----------------------------------

def is_equal(ptr_dict1: PointerDict, ptr_dict2: PointerDict) -> bool:
    """Return True if two PT dictionaries contain identical information."""
    if set(ptr_dict1.keys()) != set(ptr_dict2.keys()):
        return False
    for key, val in ptr_dict1.items():
        if key not in ptr_dict2:
            return False
        for fld, pointees in val.items():
            if fld not in ptr_dict2[key] or pointees != ptr_dict2[key][fld]:
                return False
    return True


def bind_args_to_params(ptr_dict: PointerDict, callee_ptr_dict: PointerDict,
                        param_names: list, actual_args: list) -> None:
    """
    Copy PT information from actual arguments into the callee's formal parameter
    slots.  actual_args is the list of elem objects from call.args; param_names
    is func_dict[uid][0] — the already-mangled formal parameter name strings.
    """
    for param, arg in zip(param_names, actual_args):
        if param not in callee_ptr_dict:
            continue  # scalar param — no PT info needed
        if arg.elemType == elem_types.ADR:
            # &x passed as scalar* p  →  p points to x
            callee_ptr_dict[param]['*'] = {arg.varName}
        elif arg.varName in ptr_dict:
            # pointer variable passed directly
            callee_ptr_dict[param] = copy.deepcopy(ptr_dict[arg.varName])


def merge_callee_results(ptr_dict: PointerDict,
                         callee_ptr_dict: PointerDict,
                         param_names: list) -> bool:
    """
    After analysing a callee, merge its PT information back into the caller's
    PT dictionary.  We skip formal-parameter entries (they live in the callee's
    namespace) and only propagate heap/global-side-effect information.
    Returns True if the caller's dictionary changed.
    """
    changed = False
    param_set = set(param_names)
    for var, fld_dict in callee_ptr_dict.items():
        if var in param_set:
            continue  # formal parameter — caller doesn't own this name
        if var not in ptr_dict:
            ptr_dict[var] = {}
            changed = True
        for fld, pointees in fld_dict.items():
            if fld not in ptr_dict[var]:
                ptr_dict[var][fld] = set()
            old_len = len(ptr_dict[var][fld])
            ptr_dict[var][fld].update(pointees)
            if len(ptr_dict[var][fld]) != old_len:
                changed = True
    return changed


def get_updated_func_dict(struct_dict, func_dict: dict) -> dict:
    """
    Pre-process every function: build its trimmed statement list (with CAL
    nodes included) and successor/predecessor maps.  Variable names are
    already mangled by the parser (add_funcID was called in p_func), so we
    don't mangle again here.
    """
    updated_func_dict = {}
    for func, (args, var_dict, stmt_lst) in func_dict.items():
        if func == 'main':
            # main has no parameters and is handled separately
            new_stmt_lst, successors, predecessors = get_fspta_stmts(
                struct_dict, stmt_lst, vasco=True)
            updated_func_dict[func] = ([], var_dict, new_stmt_lst,
                                       successors, predecessors)
        else:
            new_stmt_lst, successors, predecessors = get_fspta_stmts(
                struct_dict, stmt_lst, vasco=True)
            updated_func_dict[func] = (args, var_dict, new_stmt_lst,
                                       successors, predecessors)
    return updated_func_dict


def perform_vascopta(struct_dict, func_dict: dict, result_dest: str):
    """
    Entry point for context-sensitive interprocedural PTA using a VASCO-style
    worklist approach.

    func_dict layout (from parser):
        func_dict[uid] = [param_names, var_dict, stmt_lst]
    where uid is  funcName + "(type1, type2, ...)"  e.g. "foo(scalar*, scalar)"
    and 'main' maps to  ['main'] key with uid = 'main'.
    """
    updated_func_dict = get_updated_func_dict(struct_dict, func_dict)

    # context cache: maps uid -> list of (entry_ptr_dict, exit_ptr_dict)
    completed_analysis: dict[str, list] = {uid: [] for uid in func_dict}
    # tracks contexts currently on the call stack (for recursion detection)
    active_contexts: dict[str, list] = {uid: [] for uid in func_dict}

    # Initialise the main function's PT dictionary
    main_args, main_var_dict, main_stmts, main_succs, main_preds = \
        updated_func_dict['main']

    main_ptr_dict_entry = {}
    set_ptr_dict(main_var_dict, struct_dict, main_ptr_dict_entry)

    return _vasco_proc(
        struct_dict=struct_dict,
        func_dict=updated_func_dict,
        uid='main',
        entry_ptr_dict=main_ptr_dict_entry,
        result_dest=result_dest,
        active_contexts=active_contexts,
        completed_analysis=completed_analysis,
    )[0]  # return only the exit PT dict; main has no caller to receive return_pt


def _vasco_proc(struct_dict, func_dict: dict, uid: str,
                entry_ptr_dict: PointerDict, result_dest: str,
                active_contexts: dict, completed_analysis: dict) -> PointerDict:
    """
    Analyse one function invocation context.

    Returns the PT dictionary at the function's END node so the caller can
    merge side-effects back.
    """
    args, var_dict, stmt_lst, successors, predecessors = func_dict[uid]

    # return_pt accumulates the PT sets of every 'return p' statement
    # so the caller can copy them into the variable receiving the return value.
    return_pt: PointerDict = {}

    # --- Set up per-statement PT dictionaries ---
    # ptr_dicts[i] is the OUT-set for statement i.
    # Index 0 (START) is seeded with entry information; the rest start empty.
    ptr_dicts: list[PointerDict] = []
    for i in range(len(stmt_lst)):
        if i == 0:
            ptr_dicts.append(copy.deepcopy(entry_ptr_dict))
        else:
            slot: PointerDict = {}
            set_ptr_dict(var_dict, struct_dict, slot, enable_unk=False)
            # Also make room for any globals that appear in entry_ptr_dict
            for var, fld_dict in entry_ptr_dict.items():
                if var not in slot:
                    slot[var] = {fld: set() for fld in fld_dict}
            ptr_dicts.append(slot)

    # Record that we've started this context (for recursion detection)
    active_contexts[uid].append(copy.deepcopy(ptr_dicts[0]))

    # --- Fixed-point iteration ---
    iteration = 0
    changed = True
    while changed:
        changed = False
        iteration += 1

        for stmt_no, stmt in enumerate(stmt_lst):
            ptr_dict_out = ptr_dicts[stmt_no]
            old_len = nested_len_pt(ptr_dict_out)

            # Compute IN by joining predecessors' OUT sets
            pred_outs = [ptr_dicts[pred] for pred in predecessors[stmt_no]]
            set_pin(ptr_dict_out, pred_outs)

# --- NEW: JSON FILE PATHS ---
            # Force the save directory to exactly match what the GUI is looking for
            save_dir = './results/vasco/pta/'
            os.makedirs(save_dir, exist_ok=True)
            
            stmt_id = getattr(stmt, 'id', stmt_no)
            in_file = os.path.join(save_dir, f"iter_{iteration-1}stmt_{stmt_id}_in.json")
            out_file = os.path.join(save_dir, f"iter_{iteration-1}stmt_{stmt_id}_out.json")
            
            # 1. DUMP 'IN' STATE BEFORE EVALUATION
            save_vasco_json(ptr_dict_out, in_file)
            # ----------------------------

            # Handle RETURN statements — record PT info for caller
            if stmt.is_stmt_type(stmt_types.RET):
                ret_var = stmt.get_var().varName
                if ret_var in ptr_dict_out:
                    if '*' not in return_pt:
                        return_pt['*'] = set()
                    return_pt['*'].update(ptr_dict_out[ret_var].get('*', set()))
                
                # 2a. DUMP 'OUT' STATE AND CONTINUE
                save_vasco_json(ptr_dict_out, out_file)
                continue

            # Handle CALL statements interprocedurally
            if stmt.is_stmt_type(stmt_types.CAL):
                callee_uid = stmt.get_uid()   # e.g. "foo(scalar*, scalar)"

                # Check if this callee is currently on the call stack (recursion)
                recursive = any(is_equal(ctx, ptr_dict_out)
                                for ctx in active_contexts.get(callee_uid, []))
                if recursive:
                    # Conservative: leave ptr_dict_out unchanged for this iteration
                    # 2b. DUMP 'OUT' STATE AND CONTINUE
                    save_vasco_json(ptr_dict_out, out_file)
                    continue

                # Check if we already have a cached result for this exact context
                cached = None
                cached_return_pt = {}
                for (cached_entry, cached_exit, cached_ret) in completed_analysis.get(callee_uid, []):
                    if is_equal(cached_entry, ptr_dict_out):
                        cached = cached_exit
                        cached_return_pt = cached_ret
                        break

                if cached is not None:
                    callee_exit = cached
                    callee_return_pt = cached_return_pt
                else:
                    # Build a fresh entry PT dict for the callee
                    callee_args, callee_var_dict, _, _, _ = func_dict[callee_uid]
                    callee_entry: PointerDict = {}
                    set_ptr_dict(callee_var_dict, struct_dict, callee_entry)
                    # Propagate globals from caller's current PT state
                    for var, fld_dict in ptr_dict_out.items():
                        if var not in callee_entry:
                            callee_entry[var] = {fld: set() for fld in fld_dict}
                        for fld, pts in fld_dict.items():
                            callee_entry[var].setdefault(fld, set()).update(pts)
                    # Bind actual arguments to formal parameters
                    bind_args_to_params(ptr_dict_out, callee_entry,
                                        callee_args, stmt.args)
                    # Recurse
                    callee_exit, callee_return_pt = _vasco_proc(
                        struct_dict=struct_dict,
                        func_dict=func_dict,
                        uid=callee_uid,
                        entry_ptr_dict=callee_entry,
                        result_dest=result_dest,
                        active_contexts=active_contexts,
                        completed_analysis=completed_analysis,
                    )
                    completed_analysis[callee_uid].append(
                        (copy.deepcopy(ptr_dict_out), callee_exit, callee_return_pt))

                # Merge callee side-effects back into the caller's PT state
                callee_args, _, _, _, _ = func_dict[callee_uid]
                if merge_callee_results(ptr_dict_out, callee_exit, callee_args):
                    changed = True
                
                # 2c. DUMP 'OUT' STATE AND CONTINUE
                save_vasco_json(ptr_dict_out, out_file)
                continue   # don't call set_pout for a CAL node

            # Normal assignment statement
            set_pout(ptr_dict_out, stmt)

            if nested_len_pt(ptr_dict_out) != old_len:
                changed = True
                
            # 2d. DUMP 'OUT' STATE FOR NORMAL STATEMENTS
            save_vasco_json(ptr_dict_out, out_file)

    print(f"VASCO PTA — {uid}: converged in {iteration} iteration(s)")

    # Remove from active stack; cache result
    active_contexts[uid].pop()

    # Return the EXIT (END node) PT dictionary and any return value PT info
    return ptr_dicts[-1], return_pt
=======

def is_equal(ptr_dict1:PointerDict, ptr_dict2:PointerDict):
    if (len(ptr_dict1)!=len(ptr_dict2)) or (set(ptr_dict1.keys())!=set(ptr_dict2.keys())):
        return False
    
    for key, val in ptr_dict1.items():
        for key2, val2 in ptr_dict2[key].items():
            if val2!=val[key2]:
                return False
            
    return True

def add_ptr_dict(ptr_dict:PointerDict, extra_ptr_dict:PointerDict, f_args, a_args):
    init_len = len(extra_ptr_dict)
    for f, a in zip(f_args, a_args):
        ptr_dict[f] = copy.deepcopy(extra_ptr_dict[a])

    for key, val in extra_ptr_dict.items():
        if key in ptr_dict:
            flds = ptr_dict[key]
            for key1, val1 in val.items():
                flds[key1].update(val1)
        else:
            flds = {}
            for key1, val1 in val.items():
                flds[key1] = val1.copy()
            ptr_dict[key] = flds
    
    return init_len!=len(ptr_dict)

def get_updated_func_dict(struct_dict, func_dict:dict):
    updated_func_dict = {}

    func_val = {'main':0}
    count = 1
    for func in func_dict.keys():
        if func=='main':
            continue
        func_val[func] = count
        count += 1

    for func, (args, var_dict, stmt_lst) in func_dict.items():
        funcID = "_"+str(func_val[func])

        new_stmt_lst, successors, predecessors = get_fspta_stmts(struct_dict, stmt_lst, vasco=True)

        new_args = []
        for arg in args:
            new_args.append(arg+funcID)

        new_var_dict = {}
        for varName, varType in var_dict.items():
            new_var_dict[varName+funcID] = varType

        new_stmt_lst = []
        for stmt in stmt_lst:
            new_stmt = copy.deepcopy(stmt)
            new_stmt.add_funcID(funcID)
            new_stmt_lst.append(new_stmt)
        
        updated_func_dict[func] = (new_args, new_var_dict, new_stmt_lst, successors, predecessors)

    return updated_func_dict


def perform_vascopta(struct_dict, func_dict, result_dest):
    updated_func_dict = get_updated_func_dict(struct_dict, func_dict)

    startedAnalysis = {}
    completedAnalysis = {}

    for func in func_dict.keys():
        startedAnalysis[func] = []
        completedAnalysis[func] = []

    context = ('main', {}, [])

    return vasco_pta_proc(struct_dict, updated_func_dict, context, result_dest, startedAnalysis, completedAnalysis)

def vasco_pta_proc(struct_dict, func_dict, context, result_dest, startedAnalysis:dict[str, list], completedAnalysis:dict[str, list]):

    # new_stmt_lst, successors, predecessors = get_fspta_stmts(struct_dict, stmt_lst)
    args, var_dict, stmt_lst, successors, predecessors = func_dict[context[0]]

    # infoDict = {'pos_dicts':get_stmt_graph(stmt_lst, successors, result_dest+'code')}

    ptr_dicts = [{}]
    set_ptr_dict(var_dict, struct_dict, ptr_dicts[0])

    temp_ptr_dict = {}
    set_ptr_dict(var_dict, struct_dict, temp_ptr_dict, False)

    for _ in range(len(stmt_lst)-1):
        ptr_dicts.append(copy.deepcopy(temp_ptr_dict))
    del temp_ptr_dict

    check = add_ptr_dict(ptr_dicts[0], context[1], args, context[2])

    sa_ind = len(startedAnalysis[context[0]])
    startedAnalysis[context[0]].append(copy.deepcopy(ptr_dicts[0]))

    # stmt_no = 0
    # for ptr_dict in ptr_dicts:
    #     save_dict_to_json(ptr_dict, result_dest+'pta/iter_0stmt_'+str(stmt_no)+'_out.json')
    #     stmt_no += 1

    iter = 0
    change = True
    while change:
        change = False
        iter += 1

        stmt_no = 0
        for stmt in stmt_lst:
            ptr_dict_out = ptr_dicts[stmt_no]
            old_len = nested_len_pt(ptr_dict_out)

            pred_ptr_dicts = []
            for pred in predecessors[stmt_no]:
                pred_ptr_dicts.append(ptr_dicts[pred])

            set_pin(ptr_dict_out, pred_ptr_dicts)
            # save_points_to_graph(ptr_dict_out, result_dest+'pta/iter_'+str(iter)+'stmt_'+str(stmt_no)+'_in')
            # save_dict_to_json(ptr_dict_out, result_dest+'pta/iter_'+str(iter)+'stmt_'+str(stmt_no)+'_in.json')

            if stmt.is_is_stmt_type(stmt_types.CAL):
                if not change:
                    funcID = stmt.get_uid()
                    found = False
                    for sa_context in startedAnalysis[funcID]:
                        if is_equal(sa_context, ptr_dict_out):
                            found = True
                            break
                    if found:
                        break
                    found = False
                    for ca_context in completedAnalysis[funcID]:
                        if is_equal(ca_context[0], ptr_dict_out):
                            ptr_dicts[stmt_no] = copy.deepcopy(ca_context[1])
                            found = True
                    if not found:
                        ptr_dicts[stmt_no] = copy.deepcopy(vasco_pta_proc(struct_dict, func_dict, (funcID, ptr_dict_out, stmt.), result_dest, startedAnalysis, completedAnalysis))
                stmt_no += 1
                continue

            set_pout(ptr_dict_out, stmt)
            # save_points_to_graph(ptr_dict_out, result_dest+'pta/iter_'+str(iter)+'stmt_'+str(stmt_no)+'_out')
            # save_dict_to_json(ptr_dict_out, result_dest+'pta/iter_'+str(iter)+'stmt_'+str(stmt_no)+'_out.json')

            change = change or (old_len != nested_len_pt(ptr_dict_out))

            stmt_no += 1

    # print("VASCO PTA Iteration -", iter, "(confirmation)")

    # infoDict['iters'] = iter
    # save_dict_to_json(infoDict, result_dest+'info.json')

    # TODO - remove extra PT information
    # if check:

    del startedAnalysis[context[0]][sa_ind]
    completedAnalysis[context[0]].append((startedAnalysis[context[0]].pop(sa_ind), ptr_dicts[-1]))
    return ptr_dicts[-1]
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
