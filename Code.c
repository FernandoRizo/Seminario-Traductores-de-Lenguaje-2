#include <stdio.h>
int a;
int suma(int a, int b){
return a+b;
}

int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8,9);

printf("%d\n", c);  // <-- imprime 17
printf("Presiona ENTER para salir...");
getchar();
return 0;

}