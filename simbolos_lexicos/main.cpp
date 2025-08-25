#include <iostream>
#include "Pila.h"
#include "Elementos.h"

// Función de ejemplo para demostrar el uso de la pila con objetos.
void ejemplo_analizador() {
    Pila miPila;

    std::cout << "Iniciando análisis LR(1) con pila de objetos..." << std::endl;

    // El analizador siempre empieza con el estado 0 en la pila.
    miPila.push(new Estado(0));
    miPila.muestra();

    // Simulando una acción de DESPLAZAMIENTO (shift):
    // Leemos un 'id', lo metemos a la pila y luego el estado correspondiente (ej. estado 5).
    std::cout << "\nAccion: Desplazar 'id' e ir al estado 5" << std::endl;
    miPila.push(new Terminal("id"));
    miPila.push(new Estado(5));
    miPila.muestra();

    // Simulando otra acción de DESPLAZAMIENTO:
    // Leemos un '+' y vamos al estado 6.
    std::cout << "\nAccion: Desplazar '+' e ir al estado 6" << std::endl;
    miPila.push(new Terminal("+"));
    miPila.push(new Estado(6));
    miPila.muestra();

    // Simulando una acción de REDUCCIÓN (reduce):
    // Regla: F -> id (longitud 1).
    // 1. Sacamos 2*1 = 2 elementos de la pila (Estado y Terminal).
    // 2. Metemos el NoTerminal 'F'.
    // 3. Metemos el nuevo estado (ej. estado 3).
    std::cout << "\nAccion: Reducir por la regla F -> id" << std::endl;

    // Sacamos 2 elementos (Estado 5 y Terminal 'id')
    delete miPila.pop(); // Libera la memoria del estado
    delete miPila.pop(); // Libera la memoria del terminal

    // Vemos el estado que quedó en el tope (en este caso, el 6 que metimos antes).
    // El analizador usaría este estado para la tabla GOTO.
    // Asumimos que GOTO[6, F] = 3.
    miPila.push(new NoTerminal("F"));
    miPila.push(new Estado(3));
    miPila.muestra();

    std::cout << "\nAnálisis simulado completado." << std::endl;
}

int main() {
    ejemplo_analizador();
    return 0;
}
