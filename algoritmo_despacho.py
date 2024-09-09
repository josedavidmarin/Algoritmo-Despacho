import matplotlib.pyplot as plt
import numpy as np

class Proceso:
    def __init__(self, pid, tiempo_llegada, tiempo_rafaga):
        self.pid = pid
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_rafaga = tiempo_rafaga
        self.tiempo_restante = tiempo_rafaga
        self.tiempo_finalizacion = 0
        self.tiempo_espera = 0
        self.tiempo_retorno = 0

def planificacion_fifo(procesos):
    procesos.sort(key=lambda x: x.tiempo_llegada)
    tiempo_actual = 0
    grafico_gantt = []
    for proceso in procesos:
        if tiempo_actual < proceso.tiempo_llegada:
            tiempo_actual = proceso.tiempo_llegada
        grafico_gantt.append((proceso.pid, tiempo_actual, tiempo_actual + proceso.tiempo_rafaga))
        proceso.tiempo_finalizacion = tiempo_actual + proceso.tiempo_rafaga
        proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
        proceso.tiempo_espera = proceso.tiempo_retorno - proceso.tiempo_rafaga
        tiempo_actual += proceso.tiempo_rafaga
    return grafico_gantt

def planificacion_sjf(procesos):
    procesos.sort(key=lambda x: (x.tiempo_llegada, x.tiempo_rafaga))
    tiempo_actual = 0
    grafico_gantt = []
    while procesos:
        procesos_disponibles = [p for p in procesos if p.tiempo_llegada <= tiempo_actual]
        if procesos_disponibles:
            proceso = min(procesos_disponibles, key=lambda x: x.tiempo_rafaga)
            procesos.remove(proceso)
            grafico_gantt.append((proceso.pid, tiempo_actual, tiempo_actual + proceso.tiempo_rafaga))
            proceso.tiempo_finalizacion = tiempo_actual + proceso.tiempo_rafaga
            proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
            proceso.tiempo_espera = proceso.tiempo_retorno - proceso.tiempo_rafaga
            tiempo_actual += proceso.tiempo_rafaga
        else:
            tiempo_actual += 1
    return grafico_gantt

def planificacion_rr(procesos, quantum):
    tiempo_actual = 0
    cola = [p for p in procesos]
    grafico_gantt = []
    while cola:
        proceso = cola.pop(0)
        if proceso.tiempo_restante > quantum:
            grafico_gantt.append((proceso.pid, tiempo_actual, tiempo_actual + quantum))
            proceso.tiempo_restante -= quantum
            tiempo_actual += quantum
            cola.append(proceso)
        else:
            grafico_gantt.append((proceso.pid, tiempo_actual, tiempo_actual + proceso.tiempo_restante))
            tiempo_actual += proceso.tiempo_restante
            proceso.tiempo_restante = 0
            proceso.tiempo_finalizacion = tiempo_actual
            proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
            proceso.tiempo_espera = proceso.tiempo_retorno - proceso.tiempo_rafaga
    return grafico_gantt

def imprimir_tabla(procesos):
    print("PID\tTiempo Llegada\tTiempo Ráfaga\tTiempo Finalización\tTiempo Retorno\tTiempo Espera")
    for proceso in procesos:
        print(f"{proceso.pid}\t{proceso.tiempo_llegada}\t\t{proceso.tiempo_rafaga}\t\t{proceso.tiempo_finalizacion}\t\t\t{proceso.tiempo_retorno}\t\t{proceso.tiempo_espera}")

def graficar_gantt(grafico_gantt):
    fig, gantt = plt.subplots()
    gantt.set_xlabel('Tiempo')
    gantt.set_ylabel('Proceso')
    gantt.set_xticks(np.arange(0, max([x[2] for x in grafico_gantt]) + 1, 1))
    gantt.set_yticks([i + 1 for i in range(len(grafico_gantt))])
    gantt.grid(True)

    for (pid, inicio, fin) in grafico_gantt:
        gantt.broken_barh([(inicio, fin - inicio)], (pid, 1), facecolors=('tab:blue'))
        gantt.text(inicio + (fin - inicio) / 2, pid + 0.5, f"P{pid}", ha='center', va='center', color='white')
    plt.show()

def main():
    num_procesos = int(input("Introduce el número de procesos: "))
    procesos = []
    
    for i in range(num_procesos):
        tiempo_llegada = int(input(f"Introduce el tiempo de llegada del proceso {i+1}: "))
        tiempo_rafaga = int(input(f"Introduce el tiempo de ráfaga del proceso {i+1}: "))
        procesos.append(Proceso(i+1, tiempo_llegada, tiempo_rafaga))
    
    print("\nSelecciona el algoritmo de planificación:")
    print("1. Primero en llegar, primero en ser atendido (FIFO)")
    print("2. Trabajo más corto primero (SJF)")
    print("3. Round Robin (RR)")
    eleccion = int(input("Introduce tu elección: "))
    
    if eleccion == 3:
        quantum = int(input("Introduce el quantum para Round Robin: "))
        grafico_gantt = planificacion_rr(procesos, quantum)
    elif eleccion == 2:
        grafico_gantt = planificacion_sjf(procesos)
    else:
        grafico_gantt = planificacion_fifo(procesos)
    
    imprimir_tabla(procesos)
    graficar_gantt(grafico_gantt)

if __name__ == "__main__":
    main()
