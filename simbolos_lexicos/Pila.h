#pragma once
#include <list>
#include "Elementos.h"

class Pila {
private:
    std::list<ElementoPila*> lista;
public:
    void push(ElementoPila* x);
    ElementoPila* pop();
    ElementoPila* top();
    void muestra();
    ~Pila(); // Agregamos un destructor para limpiar la memoria.
};