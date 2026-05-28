import time
# 1. Capa externa: Recibe los argumentos del decorador
def timer_dec(message="Function execution time"):
    # 2. Capa intermedia: Recibe la función original
    def decorator(base_fn):
        # 3. Capa interna: Recibe los argumentos de la función original
        def enhanced_fn(*args, **kwargs):
            start = time.time()
            result = base_fn(*args, **kwargs)
            end = time.time()
            print(f"{message}: {end - start:.4f} seconds")
            return result
        return enhanced_fn
    return decorator