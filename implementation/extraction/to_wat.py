import os, glob, sys, multiprocessing

def do_work(filename, return_dict, t_id):
    return_dict['success'] = None
    _ = os.system("cargo run --quiet " + filename + " " + str(t_id))
    return_dict['success'] = True

def parse_binary_to_wat(target_file, t_id):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    for filename in [glob.glob(target_file, recursive=True)[0]]:
        proc = multiprocessing.Process(target=do_work, args=(filename, return_dict, t_id))
        proc.start()
        proc.join(timeout=30)
        proc.terminate()
    return return_dict['success']
    


