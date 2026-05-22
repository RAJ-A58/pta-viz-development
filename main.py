from parser import parse_text
from fi_pta import perform_andersens_analysis, perform_steensgaards_analysis
from fs_pta import perform_fspta
from lfcpa  import perform_lfcpa
# from vasco_pta import get_updated_func_dict
import os, shutil, sys

def perform_analysis(file_name):
    # Unpack the 3 values now returned by the updated parser
    parse_result = parse_text(file_name)
    
    if len(parse_result) == 2:
        # Fallback if an older error format tuple is returned
        return parse_result[0]

    struct_dict, func_dict, global_var_dict = parse_result

    if func_dict['main'] == 'error':
        print("PARSING ERROR:", struct_dict)  # <-- Add this print statement!
        return

    else:
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
            
        # 1. Merge global and local variable dictionaries
        local_var_dict = func_dict['main'][1]
        combined_var_dict = {**global_var_dict, **local_var_dict}
    
        # 2. Pass the combined_var_dict down to all analyses
        os.mkdir(results_dir+'/andersens')
        os.mkdir(results_dir+'/andersens/pta')
        perform_andersens_analysis(struct_dict, combined_var_dict, func_dict['main'][2], results_dir+'/andersens/')

        os.mkdir(results_dir+'/steensgaards')
        os.mkdir(results_dir+'/steensgaards/pta')
        perform_steensgaards_analysis(struct_dict, combined_var_dict, func_dict['main'][2], results_dir+'/steensgaards/')

        os.mkdir(results_dir+'/fspta')
        os.mkdir(results_dir+'/fspta/pta')
        perform_fspta(struct_dict, combined_var_dict, func_dict['main'][2],  results_dir+'/fspta/')

        os.mkdir(results_dir+'/lfcpa')
        os.mkdir(results_dir+'/lfcpa/la')
        os.mkdir(results_dir+'/lfcpa/pta')
        perform_lfcpa(struct_dict, combined_var_dict, func_dict['main'][2], results_dir+'/lfcpa/')

if __name__ == '__main__':
    
    if len(sys.argv)==2:
        file_name = sys.argv[1]
    else:
        file_name = "test.txt"
    
    with open(file_name) as f:
        perform_analysis(f.read())