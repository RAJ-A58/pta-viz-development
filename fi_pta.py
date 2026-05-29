from pta_helper import *
import graphviz

def perform_andersens_analysis(struct_dict, var_dict, stmt_lst, result_dest):
    ptr_dict = {}
<<<<<<< HEAD
    set_ptr_dict(var_dict, struct_dict, ptr_dict, False)
    new_stmt_lst = get_pta_stmts(struct_dict, stmt_lst)
    infoDict = {'pos_dicts':get_stmt_graph(new_stmt_lst, None, result_dest+'code')}
    result_dest += 'pta/iter_'
=======
    
    set_ptr_dict(var_dict, struct_dict, ptr_dict, False)
    
    new_stmt_lst = get_pta_stmts(struct_dict, stmt_lst)

    infoDict = {'pos_dicts':get_stmt_graph(new_stmt_lst, None, result_dest+'code')}

    result_dest += 'pta/iter_'

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    count = 0
    change = True
    while change:
        save_dict_to_json(ptr_dict, result_dest+str(count))
<<<<<<< HEAD
        change = False
        for stmt in new_stmt_lst:
            lhs = stmt.get_lhs()
            rhs = stmt.get_rhs()
            pointees = get_pointees(ptr_dict, rhs)
=======

        change = False

        for stmt in new_stmt_lst:
            lhs = stmt.get_lhs()
            rhs = stmt.get_rhs()
            
            pointees = get_pointees(ptr_dict, rhs)

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
            vars, fld = get_defs(ptr_dict, lhs)
            for var in vars:
                old_len = len(ptr_dict[var][fld])
                ptr_dict[var][fld].update(pointees)
                change = change or (old_len != len(ptr_dict[var][fld]))
        count += 1
<<<<<<< HEAD
    save_dict_to_json(ptr_dict, result_dest+str(count))
    print("Andersens Iteration -", count, "(confirmation)")
=======
    
    save_dict_to_json(ptr_dict, result_dest+str(count))

    print("Andersens Iteration -", count, "(confirmation)")

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    infoDict['iters'] = count
    save_dict_to_json(infoDict, result_dest+'info.json')

def perform_steensgaards_analysis(struct_dict, var_dict, stmt_lst, result_dest):
    ptr_dict = {}
    isunk_ptr_dict = {}
<<<<<<< HEAD
    var_to_set_dict = {None:None}
    set_to_var_dict = {}
=======
    var_to_set_dict = {None:None, }
    set_to_var_dict = {}

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    for var, typ in var_dict.items():
        var_to_set_dict[var] = var
        set_to_var_dict[var] = [var]
        if contains_pointer(typ, struct_dict):
            ptr_dict[var] = {}
            isunk_ptr_dict[var] = False
            if typ[-1] == '*':
                ptr_dict[var]['*'] = None
            else:
                for field, field_typ in struct_dict[typ][0].items():
                    if field_typ[-1] == '*':
                        ptr_dict[var][field] = None
<<<<<<< HEAD
    new_stmt_lst = get_pta_stmts(struct_dict, stmt_lst)
    infoDict = {'pos_dicts':get_stmt_graph(new_stmt_lst, None, result_dest+'code')}
    count = 0
    change = True
    while change:
        change = False
=======

    new_stmt_lst = get_pta_stmts(struct_dict, stmt_lst)
    infoDict = {'pos_dicts':get_stmt_graph(new_stmt_lst, None, result_dest+'code')}

    count = 0
    change = True

    while change:
        change = False

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
        count += 1
        for stmt in new_stmt_lst:
            lhs = stmt.get_lhs()
            rhs = stmt.get_rhs()
<<<<<<< HEAD
            pointee = get_pointee(ptr_dict, rhs, var_to_set_dict)
            if pointee is None:
                continue
            var, fld = get_def(ptr_dict, lhs, var_to_set_dict)
            if var is None:
                continue
=======

            pointee = get_pointee(ptr_dict, rhs, var_to_set_dict)

            if pointee is None:
                continue

            var, fld = get_def(ptr_dict, lhs, var_to_set_dict)

            if var == None:
                continue

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
            old_var = ptr_dict[var][fld]
            if old_var is None:
                ptr_dict[var][fld] = pointee
                change = True
            else:
                sets_to_unify = [pointee, var_to_set_dict[old_var]]
                change = unify(ptr_dict, sets_to_unify, var_to_set_dict, set_to_var_dict) or change
<<<<<<< HEAD
    print("Steensgaard Iteration -", count, "(confirmation)")
    infoDict['iters'] = count
    # FIX: save to correct results directory (was missing result_dest prefix)
    save_dict_to_json(infoDict, result_dest+'info.json')
    # Build and save PT graph to correct results directory
    graph_count = 0
    dot = graphviz.Digraph(
        comment="Steensgaard's PTA",
        node_attr={'colorscheme': colorscheme, 'style': 'filled'},
        edge_attr={'colorscheme': colorscheme},
        graph_attr={'rankdir': 'LR', 'bgcolor': 'transparent'},
        engine='dot'
    )
    color_dict = {}
    for node in ptr_dict.keys():
        graph_count = update_count(graph_count)
        color_dict[node] = str(graph_count)
        vars_label = '\n'.join(set_to_var_dict[node])
        dot.node(node, vars_label, color=str(graph_count))
=======

    print("Steensgaard Iteration -", count, "(confirmation)")
    
    infoDict['iters'] = count
    save_dict_to_json(infoDict, result_dest+'info.json')

    count = 0
    dot = graphviz.Digraph(comment="Steensgaard's PTA", node_attr={'colorscheme':colorscheme, 'style':'filled'}, edge_attr={'colorscheme':colorscheme}, graph_attr={'rankdir':'LR', 'bgcolor':'transparent'}, engine='dot')
    color_dict = {}

    for node in ptr_dict.keys():
        count = update_count(count)
        color_dict[node] = str(count)
        vars = '\n'.join(set_to_var_dict[node])
        dot.node(node, vars, color = str(count))

>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
    for key, val in ptr_dict.items():
        for key2, val2 in val.items():
            if val2 is None:
                continue
<<<<<<< HEAD
            label = '⁎' if key2 == '*' else key2
            dot.edge(key, var_to_set_dict[val2], label=label, color=color_dict[key])
    # FIX: render to results dir, not CWD
    dot.render(result_dest + 'pta/graph', format='svg', cleanup=True)
=======

            if key2 == '*':
                dot.edge(key, var_to_set_dict[val2], label = '⁎', color = color_dict[key])
            else:
                dot.edge(key, var_to_set_dict[val2], label = key2, color = color_dict[key])

    dot.render('steensgaard', format='svg', cleanup=True)
>>>>>>> 7986d73d2cc82cd3fb397e72dd88cb7b08d26089
