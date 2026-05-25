from parser import parse_text
from fi_pta import perform_andersens_analysis, perform_steensgaards_analysis
from fs_pta import perform_fspta
from lfcpa  import perform_lfcpa
from vasco_pta import perform_vascopta
import os, shutil, sys

def perform_analysis(file_name):
    parse_result = parse_text(file_name)

    # parse_text returns (error_str, {'main':'error'}, {}) on failure
    if len(parse_result) == 2 or parse_result[1].get('main') == 'error':
        err = parse_result[0]
        print("PARSING ERROR:", err)
        return err

    struct_dict, func_dict, global_var_dict = parse_result

    # ------------------------------------------------------------------
    # Build the combined variable dictionary for the main function.
    # Globals are visible everywhere, so we merge them with main's locals.
    # ------------------------------------------------------------------
    main_var_dict  = func_dict['main'][1]
    main_stmt_lst  = func_dict['main'][2]
    combined_var_dict = {**global_var_dict, **main_var_dict}

    # ------------------------------------------------------------------
    # Prepare results directory
    # ------------------------------------------------------------------
    results_dir = './results'
    if os.path.exists(results_dir):
        for filename in os.listdir(results_dir):
            file_path = os.path.join(results_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        os.mkdir(results_dir)

    # ------------------------------------------------------------------
    # 1. Flow-insensitive analyses (main only — intra-procedural)
    # ------------------------------------------------------------------
    os.makedirs(results_dir + '/andersens/pta', exist_ok=True)
    perform_andersens_analysis(
        struct_dict, combined_var_dict, main_stmt_lst,
        results_dir + '/andersens/')

    os.makedirs(results_dir + '/steensgaards/pta', exist_ok=True)
    perform_steensgaards_analysis(
        struct_dict, combined_var_dict, main_stmt_lst,
        results_dir + '/steensgaards/')

    # ------------------------------------------------------------------
    # 2. Flow-sensitive intra-procedural PTA
    # ------------------------------------------------------------------
    os.makedirs(results_dir + '/fspta/pta', exist_ok=True)
    perform_fspta(
        struct_dict, combined_var_dict, main_stmt_lst,
        results_dir + '/fspta/')

    # ------------------------------------------------------------------
    # 3. LFCPA (intra-procedural, shown in GUI)
    # ------------------------------------------------------------------
    os.makedirs(results_dir + '/lfcpa/la',  exist_ok=True)
    os.makedirs(results_dir + '/lfcpa/pta', exist_ok=True)
    perform_lfcpa(
        struct_dict, combined_var_dict, main_stmt_lst,
        results_dir + '/lfcpa/')

    # ------------------------------------------------------------------
    # 4. VASCO context-sensitive interprocedural PTA
    #    Receives the full func_dict so it can follow call edges.
    #    We update func_dict['main'][1] to include globals before passing.
    # ------------------------------------------------------------------
    has_calls = any(
        s.is_stmt_type(4)          # stmt_types.CAL == 4
        for s in main_stmt_lst[1:-1]
    )
    if has_calls or len(func_dict) > 1:
        os.makedirs(results_dir + '/vasco/pta', exist_ok=True)
        # Give 'main' the combined var dict so globals are visible
        func_dict_for_vasco = dict(func_dict)
        main_entry = list(func_dict['main'])
        main_entry[1] = combined_var_dict
        func_dict_for_vasco['main'] = main_entry
        perform_vascopta(struct_dict, func_dict_for_vasco,
                         results_dir + '/vasco/')
    else:
        print("No function calls found — skipping VASCO interprocedural analysis.")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        file_name = "test.txt"

    with open(file_name) as f:
        perform_analysis(f.read())