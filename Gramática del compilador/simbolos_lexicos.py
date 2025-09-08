# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class ElementoPila(ABC):
    """
    Clase base abstracta para los elementos de la pila.
    Define una interfaz común para todos los elementos.
    """
    @abstractmethod
    def __str__(self):
        """
        Método que debe ser implementado por las clases hijas para
        definir su representación como cadena de texto.
        """
        pass

class Estado(ElementoPila):
    """Representa un ESTADO en la pila (ej. 0, 4, 9)."""
    def __init__(self, id_estado):
        self.id = id_estado

    def __str__(self):
        return str(self.id)

class Terminal(ElementoPila):
    """Representa un SÍMBOLO TERMINAL en la pila (ej. 'id', '+', '$')."""
    def __init__(self, simbolo):
        self.simbolo = simbolo

    def __str__(self):
        return self.simbolo

class NoTerminal(ElementoPila):
    """Representa un SÍMBOLO NO TERMINAL en la pila (ej. 'E', 'T', 'F')."""
    def __init__(self, simbolo):
        self.simbolo = simbolo

    def __str__(self):
        return self.simbolo

class Pila:
    """
    Implementación de una Pila que almacena objetos de tipo ElementoPila.
    """
    def __init__(self):
       
        self._elementos = []

    def push(self, elemento):
        """Añade un elemento al tope de la pila."""
        self._elementos.append(elemento)

    def pop(self):
        """Elimina y devuelve el elemento del tope de la pila."""
        if not self.is_empty():
            return self._elementos.pop()
        return None 

    def top(self):
        """Devuelve el elemento del tope de la pila sin eliminarlo."""
        if not self.is_empty():
            return self._elementos[-1]
        return None 

    def is_empty(self):
        """Verifica si la pila está vacía."""
        return len(self._elementos) == 0
    
    def __str__(self):
        """
        Crea una representación en cadena de la pila, mostrando los
        elementos desde el fondo hasta el tope.
        """
       
        contenido = " ".join(str(e) for e in self._elementos)
        return f"PILA: $ {contenido}"


if __name__ == '__main__':
    
    mi_pila = Pila()

    print("Iniciando análisis LR(1) con pila de objetos en Python...")

    # El analizador siempre empieza con el estado 0 en la pila.
    mi_pila.push(Estado(0))
    print(mi_pila)

    # DESPLAZAMIENTO (shift):
    # Leemos un 'id', lo metemos a la pila y luego el estado correspondiente (ej. estado 5).
    print("\nAccion: Desplazar 'id' e ir al estado 5")
    mi_pila.push(Terminal("id"))
    mi_pila.push(Estado(5))
    print(mi_pila)

   
    print("\nAccion: Desplazar '+' e ir al estado 6")
    mi_pila.push(Terminal("+"))
    mi_pila.push(Estado(6))
    print(mi_pila)

   
    print("\nAccion: Reducir por la regla F -> id")
    
    
    mi_pila.pop() 
    mi_pila.pop() 
    
    # Estado de la pila: $ 0 id 5 + 6
 
    print("\n--- Corrección de la simulación ---")
    print("Accion: Desplazar 'id' e ir al estado 4")
    mi_pila.push(Terminal("id"))
    mi_pila.push(Estado(4))
    print(mi_pila) 
    # Pila: $ 0 id 5 + 6 id 4
    
    print("\nAccion: Reducir por la regla F -> id")
    mi_pila.pop() 
    mi_pila.pop() 
    
    #  (Estado 6)
    #
    mi_pila.push(NoTerminal("F"))
    mi_pila.push(Estado(3))
    print(mi_pila) 
    # Pila: $ 0 id 5 + 6 F 3
    
    print("\nAnálisis simulado completado.")