from multiprocessing import Pool
from tqdm import tqdm

def parallelize(func, args, ncores):
    with Pool(ncores) as pool:
        # imap_unordered devuelve un iterador inmediato, permitiendo que tqdm se actualice uno a uno
        results = list(tqdm(pool.imap_unordered(func, args), total=len(args)))
    return results