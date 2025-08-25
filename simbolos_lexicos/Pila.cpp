#include "Pila.h"
#include <iostream>

// Mete un puntero a un elemento en la pila
void Pila::push(ElementoPila* x) {
    lista.push_front(x);
}

// Saca un puntero de la pila y lo devuelve
ElementoPila* Pila::pop() {
    if (lista.empty()) return nullptr;
    ElementoPila* x = lista.front();
    lista.pop_front();
    return x;
}

// Devuelve el elemento del tope de la pila sin sacarlo
ElementoPila* Pila::top() {
    if (lista.empty()) return nullptr;
    return lista.front();
}

// Muestra el contenido de la pila de abajo hacia arriba
void Pila::muestra() {
    std::cout << "PILA: $ ";
    // Usamos un iterador reverso para imprimir desde el fondo (rbegin) hasta el tope (rend)
    for (auto it = lista.rbegin(); it != lista.rend(); ++it) {
        (*it)->muestra(); // Llama al método muestra() del objeto (Estado, Terminal, etc.)
        std::cout << " ";
    }
    std::cout << std::endl;
}

// Destructor para liberar la memoria de los objetos restantes en la pila
Pila::~Pila() {
    while (!lista.empty()) {
        delete pop(); // Llama a pop() y elimina el puntero devuelto
    }
}