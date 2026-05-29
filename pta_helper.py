from helper import *
from copy import deepcopy
from stmt_helper import *

def get_fspta_stmts(struct_dict, stmt_lst:list[stmt], lb = False, vasco = False):
    new_stmt_lst = [stmt_lst[0]]
<<<<<<< HEAD
=======

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    counter_lst = [None]*(len(stmt_lst)+1)
    counter_lst[0] = 0
    counter_lst[-2] = len(counter_lst)-2
    counter_lst[-1] = len(counter_lst)-1
<<<<<<< HEAD
=======

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    counter = 1
    new_stmt_counter = 1
    counter_to_stmt = {0:0}
    stmt_to_counter = {0:0}
    for stmt in stmt_lst[1:-1]:
        match stmt.stmtType:
            case stmt_types.ASG:
                check = contains_pointer(stmt.get_type(), struct_dict)
                lhs = stmt.get_lhs()
                rhs = stmt.get_rhs()
                if check or (lb and (lhs.is_elem_type(elem_types.FLP) or (rhs.elemType in [elem_types.FLP, elem_types.PTR]))):
<<<<<<< HEAD
                    stmt.containsPointer = check
                    new_stmt_lst.append(stmt)
=======
                    # if lb:
                    #     new_stmt_lst.append(['ASG', lhs, rhs, check])
                    # else:
                    #     new_stmt_lst.append(['ASG', lhs, rhs])
                    # new_stmt_lst.append(['ASG', lhs, rhs, check]) #TODO
                    stmt.containsPointer = check
                    new_stmt_lst.append(stmt)
                    
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
                    counter_lst[counter] = counter
                    counter_to_stmt[counter] = new_stmt_counter
                    stmt_to_counter[new_stmt_counter] = counter
                    new_stmt_counter += 1
            case stmt_types.GOT:
                if counter == stmt.get_lno():
                    counter_lst[counter] = -1
                else:
                    counter_lst[counter] = stmt.get_lno()
            case stmt_types.IF:
                new_stmt_lst.append(stmt)
                counter_lst[counter] = counter
                counter_to_stmt[counter] = new_stmt_counter
                stmt_to_counter[new_stmt_counter] = counter
                new_stmt_counter += 1
            case stmt_types.USE:
<<<<<<< HEAD
                if lb:
=======
                # if lb and (stmt[1][0][-1] == '*'):
                if lb:
                    # new_stmt_lst.append(['USE', stmt[1][1]])
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
                    new_stmt_lst.append(stmt)
                    counter_lst[counter] = counter
                    counter_to_stmt[counter] = new_stmt_counter
                    stmt_to_counter[new_stmt_counter] = counter
                    new_stmt_counter += 1
            case stmt_types.CAL:
                if vasco:
                    new_stmt_lst.append(stmt)
                    counter_lst[counter] = counter
                    counter_to_stmt[counter] = new_stmt_counter
                    stmt_to_counter[new_stmt_counter] = counter
                    new_stmt_counter += 1
<<<<<<< HEAD
            case stmt_types.RET:
                if vasco:
                    new_stmt_lst.append(stmt)
                    counter_lst[counter] = counter
                    counter_to_stmt[counter] = new_stmt_counter
                    stmt_to_counter[new_stmt_counter] = counter
                    new_stmt_counter += 1
        counter += 1
    new_stmt_lst.append(stmt_lst[-1])
    counter_to_stmt[counter] = new_stmt_counter
    stmt_to_counter[new_stmt_counter] = counter
    new_stmt_lst.append(plain_text('loop'))
    counter_to_stmt[counter + 1] = new_stmt_counter + 1
    stmt_to_counter[new_stmt_counter + 1] = counter + 1
    successors = [None]*len(new_stmt_lst)
=======
        counter += 1
    
    new_stmt_lst.append(stmt_lst[-1])
    counter_to_stmt[counter] = new_stmt_counter
    stmt_to_counter[new_stmt_counter] = counter

    new_stmt_lst.append(plain_text('loop'))
    counter_to_stmt[counter + 1] = new_stmt_counter + 1
    stmt_to_counter[new_stmt_counter + 1] = counter + 1

    successors = [None]*len(new_stmt_lst)

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    predecessors = [[] for _ in range(len(new_stmt_lst))]
    new_stmt_counter = 0
    for stmt in new_stmt_lst[0:-2]:
        if stmt.stmtType == stmt_types.IF:
            succ1 = counter_to_stmt[get_next_counter(stmt_to_counter[new_stmt_counter]+1, counter_lst)]
            succ2 = counter_to_stmt[get_next_counter(stmt.get_lno(), counter_lst)]
            successors[new_stmt_counter] = [succ1, succ2]
            predecessors[succ1].append(new_stmt_counter)
            predecessors[succ2].append(new_stmt_counter)
        else:
            succ = counter_to_stmt[get_next_counter(stmt_to_counter[new_stmt_counter]+1, counter_lst)]
            successors[new_stmt_counter] = [succ]
            predecessors[succ].append(new_stmt_counter)
        new_stmt_counter += 1
<<<<<<< HEAD
=======

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    if len(predecessors[-1]) == 0:
        new_stmt_lst.pop()
        predecessors.pop()
        successors.pop()
<<<<<<< HEAD
=======

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    return (new_stmt_lst, successors, predecessors)

def get_pta_stmts(struct_dict, stmt_lst:list[stmt]):
    new_stmt_lst = []
    for stmt in stmt_lst[1:-1]:
        if stmt.is_stmt_type(stmt_types.ASG):
            if contains_pointer(stmt.get_type(), struct_dict):
                new_stmt_lst.append(stmt)
    return new_stmt_lst

def get_defs(ptr_dict:PointerDict, lhs:variable|field):
    vars = []
    fld = ''
    match lhs.elemType:
        case elem_types.VAR:
            vars.append(lhs.varName)
            fld = '*'
        case elem_types.PTR:
<<<<<<< HEAD
            if lhs.varName not in ptr_dict:
                return ([], '*')
=======
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
            for var in (ptr_dict[lhs.varName]['*'] - {'?'}):
                vars.append(var)
            fld = '*'
        case elem_types.FLP:
<<<<<<< HEAD
            if lhs.varName not in ptr_dict:
                return ([], '')
=======
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
            for var in (ptr_dict[lhs.varName]['*'] - {'?'}):
                vars.append(var)
            fld = lhs.fld
        case elem_types.FLD:
            vars.append(lhs.varName)
            fld = lhs.fld
    return (vars, fld)

def get_pointees(ptr_dict:PointerDict, rhs:variable|field):
    pointees = set()
    match rhs.elemType:
        case elem_types.ADR:
            pointees.add(rhs.varName)
        case elem_types.VAR:
<<<<<<< HEAD
            if rhs.varName not in ptr_dict:
                return pointees
            for var in ptr_dict[rhs.varName]['*']:
                pointees.add(var)
        case elem_types.PTR:
            if rhs.varName not in ptr_dict:
                return pointees
            for q in ptr_dict[rhs.varName]['*']:
                if q == '?':
                    pointees.add('?')
                elif q in ptr_dict:
                    for var in ptr_dict[q]['*']:
                        pointees.add(var)
        case elem_types.FLP:
            if rhs.varName not in ptr_dict:
                return pointees
=======
            for var in ptr_dict[rhs.varName]['*']:
                pointees.add(var)
        case elem_types.PTR:
            for q in ptr_dict[rhs.varName]['*']:
                if q == '?':
                    pointees.add('?')
                else:
                    for var in ptr_dict[q]['*']:
                        pointees.add(var)
        case elem_types.FLP:
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
            fld = rhs.fld
            for var1 in ptr_dict[rhs.varName]['*']:
                if var1 == '?':
                    pointees.add('?')
<<<<<<< HEAD
                elif var1 in ptr_dict:
                    for var2 in ptr_dict[var1][fld]:
                        pointees.add(var2)
        case elem_types.FLD:
            if rhs.varName not in ptr_dict:
                return pointees
=======
                else:
                    for var2 in ptr_dict[var1][fld]:
                        pointees.add(var2)
        case elem_types.FLD:
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
            for var in ptr_dict[rhs.varName][rhs.fld]:
                pointees.add(var)
        case elem_types.MAL:
            pointees.add(rhs.varName)
    return pointees

def get_pointee(ptr_dict:PointerDict, rhs:variable|field, var_to_set_dict):
    pointee = None
    rhs_var = var_to_set_dict[rhs.varName]
    match rhs.elemType:
        case elem_types.ADR:
            pointee = rhs_var
        case elem_types.VAR:
            pointee = var_to_set_dict[ptr_dict[rhs_var]['*']]
        case elem_types.PTR:
            pointee = ptr_dict[rhs_var]['*']
            if pointee != None:
                pointee = var_to_set_dict[ptr_dict[var_to_set_dict[pointee]]['*']]
        case elem_types.FLP:
            pointee = ptr_dict[rhs_var]['*']
            if pointee != None:
                fld = rhs.fld
                pointee = var_to_set_dict[ptr_dict[var_to_set_dict[pointee]][fld]]
        case elem_types.FLD:
            pointee = var_to_set_dict[ptr_dict[rhs_var][rhs.fld]]
        case elem_types.MAL:
            pointee = rhs_var
    return pointee

def get_def(ptr_dict:PointerDict, lhs:variable|field, var_to_set_dict):
    var = None
    fld = ''
    lhs_var = var_to_set_dict[lhs.varName]
    match lhs.elemType:
        case elem_types.VAR:
            var = lhs_var
            fld = '*'
        case elem_types.PTR:
            var = var_to_set_dict[ptr_dict[lhs_var]['*']]
            fld = '*'
        case elem_types.FLP:
            var = var_to_set_dict[ptr_dict[lhs_var]['*']]
            fld = lhs.fld
        case elem_types.FLD:
            var = lhs_var
            fld = lhs.fld
    return (var, fld)

def set_ptr_dict(var_dict, struct_dict, ptr_dict:PointerDict, enable_unk = True):
    int_set = set()
    if enable_unk:
        int_set.add('?')
<<<<<<< HEAD
    for var, typ in var_dict.items():
        if contains_pointer(typ, struct_dict):
            ptr_dict[var] = {}
=======

    for var, typ in var_dict.items():
        if contains_pointer(typ, struct_dict):
            ptr_dict[var] = {}
            
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
            if typ[-1] == '*':
                ptr_dict[var]['*'] = int_set.copy()
            else:
                for field in struct_dict[typ][0].keys():
                    ptr_dict[var][field] = int_set.copy()

def unify(ptr_dict:PointerDict, sets_to_unify, var_to_set_dict, set_to_var_dict):
    if sets_to_unify[0] == sets_to_unify[1]:
        return False
    else:
        new_set = sets_to_unify[0]
        unified_set = sets_to_unify[1]
<<<<<<< HEAD
        set_to_var_dict[new_set].extend(set_to_var_dict.pop(unified_set))
        for var, old_set in var_to_set_dict.items():
            if old_set == unified_set:
                var_to_set_dict[var] = new_set
        if new_set not in ptr_dict:
            return False
=======

        set_to_var_dict[new_set].extend(set_to_var_dict.pop(unified_set))

        for var, old_set in var_to_set_dict.items():
            if old_set == unified_set:
                var_to_set_dict[var] = new_set

        if new_set not in ptr_dict:
            return False

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
        new_sets_to_unify_dict = {}
        for fld, var in ptr_dict[new_set].items():
            if var != None:
                new_sets_to_unify_dict[fld] = [var_to_set_dict[var]]
            else:
                new_sets_to_unify_dict[fld] = []
<<<<<<< HEAD
        sets_to_unify = list(sets_to_unify)
=======

        sets_to_unify = list(sets_to_unify)

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
        for fld, var in ptr_dict[unified_set].items():
            if var != None:
                new_sets_to_unify_dict[fld].append(var_to_set_dict[var])
        del ptr_dict[unified_set]
<<<<<<< HEAD
        change = False
=======

        change = False

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
        for new_sets_to_unify in new_sets_to_unify_dict.values():
            if len(new_sets_to_unify) != 2:
                continue
            change = unify(ptr_dict, new_sets_to_unify, var_to_set_dict, set_to_var_dict) or change
<<<<<<< HEAD
=======

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
        return change

def get_must_pt(ptr_dict:PointerDict, ptr:str, fld:str):
    ptrs = ptr_dict[ptr][fld]
    if len(ptrs) > 1:
        return []
    elif len(ptrs) == 1 and '?' not in ptrs:
        return list(ptrs)
    else:
        return ['$all']

def get_strong_update(ptr_dict:PointerDict, lhs:variable|field):
    vars = []
    fld = ''
<<<<<<< HEAD
=======

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    match lhs.elemType:
        case elem_types.VAR:
            vars.append(lhs.varName)
            fld = '*'
        case elem_types.PTR:
<<<<<<< HEAD
            if lhs.varName in ptr_dict:
                vars.extend(get_must_pt(ptr_dict, lhs.varName, '*'))
            fld = '*'
        case elem_types.FLP:
            if lhs.varName in ptr_dict:
                vars.extend(get_must_pt(ptr_dict, lhs.varName, '*'))
=======
            vars.extend(get_must_pt(ptr_dict, lhs.varName, '*'))
            fld = '*'
        case elem_types.FLP:
            vars.extend(get_must_pt(ptr_dict, lhs.varName, '*'))
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
            fld = lhs.fld
        case elem_types.FLD:
            vars.append(lhs.varName)
            fld = lhs.fld
    return (vars, fld)

def set_pin(ptr_dict_in:PointerDict, ptr_dicts:list[PointerDict]):
    for ptr in ptr_dict_in.keys():
        for fld in ptr_dict_in[ptr].keys():
            for ptr_dict in ptr_dicts:
<<<<<<< HEAD
                if ptr in ptr_dict and fld in ptr_dict[ptr]:
                    ptr_dict_in[ptr][fld].update(ptr_dict[ptr][fld])
=======
                ptr_dict_in[ptr][fld].update(ptr_dict[ptr][fld])
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089

def set_lb_pin(ptr_dict_in:PointerDict, ptr_dicts:PointerDict, liveness_dict:LivenessDict):
    for ptr, ptr_dict in ptr_dict_in.items():
        for fld, fld_dict in ptr_dict.items():
            fld_dict.clear()
            if ptr not in liveness_dict[fld]:
                continue
<<<<<<< HEAD
            for pd in ptr_dicts:
                if ptr in pd and fld in pd[ptr]:
                    fld_dict.update(pd[ptr][fld])
=======
            for ptr_dict in ptr_dicts:
                fld_dict.update(ptr_dict[ptr][fld])
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089

def set_pout(ptr_dict_out:PointerDict, stmt:assignment):
    if not stmt.is_stmt_type(stmt_types.ASG):
        return
<<<<<<< HEAD
    lhs = stmt.get_lhs()
    rhs = stmt.get_rhs()
    pointees = get_pointees(ptr_dict_out, rhs)
    vars, fld = get_defs(ptr_dict_out, lhs)
    if not fld:
        return
=======
    
    lhs = stmt.get_lhs()
    rhs = stmt.get_rhs()

    pointees = get_pointees(ptr_dict_out, rhs)
    vars, fld = get_defs(ptr_dict_out, lhs)

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    su_vars, su_fld = get_strong_update(ptr_dict_out, lhs)
    for su_var in su_vars:
        if su_var == '$all':
            for var in ptr_dict_out.values():
                if su_fld in var:
                    var[su_fld].clear()
<<<<<<< HEAD
        elif su_var in ptr_dict_out and su_fld in ptr_dict_out[su_var]:
            ptr_dict_out[su_var][su_fld].clear()
    for var in vars:
        if var in ptr_dict_out and fld in ptr_dict_out[var]:
            ptr_dict_out[var][fld].update(pointees)
=======
        else:
            ptr_dict_out[su_var][su_fld].clear()

    for var in vars:
        ptr_dict_out[var][fld].update(pointees)
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089

def set_lb_pout(ptr_dict_out:PointerDict, stmt:stmt|assignment, liveness_dict:LivenessDict, ptr_dict_in:PointerDict):
    ptr_dict_out |= deepcopy(ptr_dict_in)
    for ptr, ptr_dict in ptr_dict_out.items():
        for fld, pti in ptr_dict.items():
            if ptr not in liveness_dict[fld]:
                pti.clear()
<<<<<<< HEAD
    if (not stmt.is_stmt_type(stmt_types.ASG)) or not stmt.containsPointer:
        return
    lhs = stmt.get_lhs()
    rhs = stmt.get_rhs()
    pointees = get_pointees(ptr_dict_in, rhs)
    vars, fld = get_defs(ptr_dict_in, lhs)
    if not fld:
        return
    su_vars, su_fld = get_strong_update(ptr_dict_in, lhs)
=======

    if (not stmt.is_stmt_type(stmt_types.ASG)) or not stmt.containsPointer:
        return
    
    lhs = stmt.get_lhs()
    rhs = stmt.get_rhs()

    pointees = get_pointees(ptr_dict_in, rhs)
    vars, fld = get_defs(ptr_dict_in, lhs)

    su_vars, su_fld = get_strong_update(ptr_dict_in, lhs)

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    for su_var in su_vars:
        if su_var == '$all':
            for var in ptr_dict_out.values():
                if su_fld in var:
                    var[su_fld].clear()
<<<<<<< HEAD
        elif su_var in ptr_dict_out and su_fld in ptr_dict_out[su_var]:
            ptr_dict_out[su_var][su_fld].clear()
    for var in liveness_dict[fld].intersection(vars):
        if var in ptr_dict_out and fld in ptr_dict_out[var]:
            ptr_dict_out[var][fld].update(pointees)
=======
        else:
            ptr_dict_out[su_var][su_fld].clear()
    
    for var in liveness_dict[fld].intersection(vars):
        ptr_dict_out[var][fld].update(pointees)
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089

def set_lhsref(lhsref, lhs:variable|field, check = False):
    if lhs.elemType in [elem_types.PTR, elem_types.FLP]:
        lhsref['*'] = [lhs.varName]
    elif check:
        lhsref['*'] = []

def set_lhsrhsref(ref, stmt:assignment, ptr_dict:PointerDict):
    set_lhsref(ref, stmt.get_lhs(), True)
    rhs = stmt.get_rhs()
    check = stmt.containsPointer
    match rhs.elemType:
        case elem_types.VAR:
            ref['*'].append(rhs.varName)
        case elem_types.PTR:
            ref['*'].append(rhs.varName)
<<<<<<< HEAD
            if check and rhs.varName in ptr_dict:
                ref['*'].extend(ptr_dict[rhs.varName]['*'])
        case elem_types.FLP:
            ref['*'].append(rhs.varName)
            if check and rhs.varName in ptr_dict:
=======
            if check:
                ref['*'].extend(ptr_dict[rhs.varName]['*'])
        case elem_types.FLP:
            ref['*'].append(rhs.varName)
            if check:
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
                fld = rhs.fld
                qs = ptr_dict[rhs.varName][fld]
                if len(qs) != 0:
                    ref[fld] = []
                    ref[fld].extend(qs)
        case elem_types.FLD:
            ref[rhs.fld] = [rhs.varName]
            if len(ref['*']) == 0:
                del ref['*']

def get_ref(stmt:stmt|assignment|use, ptr_dict:PointerDict, liveness_dict:LivenessDict):
    ref = {}
    if stmt.is_stmt_type(stmt_types.ASG):
        lhs = stmt.get_lhs()
        vars, fld = get_defs(ptr_dict, lhs)
<<<<<<< HEAD
        if not fld:
            return ref
=======
        
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
        if liveness_dict[fld].isdisjoint(vars):
            if sum(len(x) for x in liveness_dict.values()) != 0:
                set_lhsref(ref, lhs)
        else:
            set_lhsrhsref(ref, stmt, ptr_dict)
<<<<<<< HEAD
    elif stmt.is_stmt_type(stmt_types.USE):
        ref['*'] = [stmt.varName]
=======

    elif stmt.is_stmt_type(stmt_types.USE):
        ref['*'] = [stmt.varName]

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    return ref

def set_lin(liveness_dict_in:LivenessDict, stmt:stmt|assignment|use, ptr_dict:PointerDict, liveness_dict_out:LivenessDict):
    ref = get_ref(stmt, ptr_dict, liveness_dict_out)
<<<<<<< HEAD
    liveness_dict_in |= deepcopy(liveness_dict_out)
    if stmt.is_stmt_type(stmt_types.ASG) and stmt.containsPointer:
        vars, fld = get_strong_update(ptr_dict, stmt.get_lhs())
=======
    
    liveness_dict_in |= deepcopy(liveness_dict_out)

    if stmt.is_stmt_type(stmt_types.ASG) and stmt.containsPointer:
        vars, fld = get_strong_update(ptr_dict, stmt.get_lhs())

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
        if vars == ['$all']:
            liveness_dict_in[fld].clear()
        else:
            liveness_dict_in[fld].difference_update(vars)
<<<<<<< HEAD
=======

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    for fld, vars in ref.items():
        liveness_dict_in[fld].update(vars)

def set_lout(liveness_dict_out:LivenessDict, liveness_dicts:LivenessDict):
    for fld, fld_dict in liveness_dict_out.items():
        fld_dict.clear()
        for liveness_dict in liveness_dicts:
            fld_dict.update(liveness_dict[fld])