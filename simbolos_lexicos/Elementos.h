#pragma once
#include <iostream>
#include <string>

// Clase base abstracta para todos los elementos de la pila.
class ElementoPila {
public:
    // "virtual" permite que las clases hijas anulen este método.
    // "= 0" lo hace un "método virtual puro", obligando a las clases hijas a implementarlo.
    virtual void muestra() = 0; 
    
    // Un destructor virtual es crucial cuando se trabaja con herencia y punteros.
    // Asegura que se llame al destructor correcto al eliminar un objeto.
    virtual ~ElementoPila() {} 
};

// Clase para representar ESTADOS (ej. 0, 1, 4)
class Estado : public ElementoPila {
private:
    int id;
public:
    Estado(int id) : id(id) {}
    int getId() { return id; }
    void muestra() override {
        std::cout << id; // Los estados se muestran como su número
    }
};

// Clase para representar SÍMBOLOS TERMINALES (ej. +, *, id)
class Terminal : public ElementoPila {
private:
    std::string simbolo;
public:
    Terminal(std::string s) : simbolo(s) {}
    std::string getSimbolo() { return simbolo; }
    void muestra() override {
        std::cout << simbolo; // Los terminales se muestran como su símbolo
    }
};

// Clase para representar SÍMBOLOS NO TERMINALES (ej. E, T, F)
class NoTerminal : public ElementoPila {
private:
    std::string simbolo;
public:
    NoTerminal(std::string s) : simbolo(s) {}
    std::string getSimbolo() { return simbolo; }
    void muestra() override {
        std::cout << simbolo; // Los no terminales también se muestran como su símbolo
    }
};