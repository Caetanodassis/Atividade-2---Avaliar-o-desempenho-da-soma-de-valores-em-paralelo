import multiprocessing
import time
import os

def somar_bloco_binario(caminho, inicio, fim):
    """Lê o intervalo de bytes e soma os números encontrados."""
    soma_local = 0.0
    try:
        with open(caminho, 'rb') as f:
            f.seek(inicio)
            # Lê o bloco definido pelo intervalo
            corpo = f.read(fim - inicio)
            # Transforma bytes em string e separa os números
            numeros = corpo.split()
            for num in numeros:
                try:
                    soma_local += float(num)
                except ValueError:
                    continue
    except Exception as e:
        print(f"Erro no processo: {e}")
    return soma_local

def calcular_parallel(caminho, num_processos):
    tamanho_total = os.path.getsize(caminho)
    intervalos = []
    
    with open(caminho, 'rb') as f:
        inicio_atual = 0
        for i in range(num_processos):
            if i == num_processos - 1:
                # O último bloco vai até o fim do arquivo
                fim_atual = tamanho_total
            else:
                # Pula para a posição teórica de corte
                f.seek(inicio_atual + (tamanho_total // num_processos))
                # Avança até o próximo \n para garantir integridade do número
                f.readline()
                fim_atual = f.tell()
            
            intervalos.append((inicio_atual, fim_atual))
            inicio_atual = fim_atual

    inicio_cronometro = time.perf_counter()
    
    # Pool de processos para execução paralela
    with multiprocessing.Pool(processes=num_processos) as pool:
        # Prepara argumentos para os processos
        args = [(caminho, start, end) for start, end in intervalos]
        resultados = pool.starmap(somar_bloco_binario, args)
        soma_total = sum(resultados)
        
    fim_cronometro = time.perf_counter()
    return soma_total, (fim_cronometro - inicio_cronometro)

if __name__ == "__main__":
    caminho_txt = r"C:\Users\aluno\Downloads\trabalho 2\numero1.txt"
    
    if not os.path.exists(caminho_txt):
        print(f"Arquivo não encontrado: {caminho_txt}")
    else:
        # Detecta quantos núcleos a máquina possui
        nucleos = multiprocessing.cpu_count()
        print(f"Processador detectado com {nucleos} núcleos lógicos.")
        
        testes = [1, 2, 4, 8, 12]
        
        print(f"\n{'='*55}")
        print(f"{'THREADS':<10} | {'TEMPO (s)':<12} | {'SOMA TOTAL'}")
        print(f"{'-'*55}")
        
        for t in testes:
            resultado, tempo = calcular_parallel(caminho_txt, t)
            print(f"{t:<10} | {tempo:<12.4f} | {resultado:.2f}")
        
        print(f"{'='*55}")
