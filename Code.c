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
}

//Árbol generado

/*
[000] [E0 tipo E1]                                                  ⟂ tipo        act=  1  shift → estado 1
[001] [E0 tipo E1 identificador E7]                                 ⟂ identificador  act=  7  shift → estado 7
[002] [E0 VarDecl E5]                                               ⟂ ;           act= -7  reduce R6: VarDecl (|rhs|=2) → goto 5
[003] [E0 VarDecl E5 ; E9]                                          ⟂ ;           act=  9  shift → estado 9
[004] [E0 Decl E4]                                                  ⟂ tipo        act= -5  reduce R4: Decl (|rhs|=2) → goto 4
[005] [E0 DeclList E3]                                              ⟂ tipo        act= -4  reduce R3: DeclList (|rhs|=1) → goto 3
[006] [E0 DeclList E3 tipo E1]                                      ⟂ tipo        act=  1  shift → estado 1
[007] [E0 DeclList E3 tipo E1 identificador E7]                     ⟂ identificador  act=  7  shift → estado 7
[008] [E0 DeclList E3 tipo E1 identificador E7 ( E10]               ⟂ (           act= 10  shift → estado 10
[009] [E0 DeclList E3 tipo E1 identificador E7 ( E10 tipo E11]      ⟂ tipo        act= 11  shift → estado 11
[010] [E0 DeclList E3 tipo E1 identificador E7 ( E10 tipo E11 identificador E15]  ⟂ identificador  act= 15  shift → estado 15
[011] [E0 DeclList E3 tipo E1 identificador E7 ( E10 Param E14]     ⟂ ,           act=-13  reduce R12: Param (|rhs|=2) → goto 14
[012] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamList E13]  ⟂ ,           act=-11  reduce R10: ParamList (|rhs|=1) → goto 13
[013] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamList E13 , E17]  ⟂ ,           act= 17  shift → estado 17
[014] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamList E13 , E17 tipo E11]  ⟂ tipo        act= 11  shift → estado 11
[015] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamList E13 , E17 tipo E11 identificador E15]  ⟂ identificador  act= 15  shift → estado 15
[016] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamList E13 , E17 Param E20]  ⟂ )           act=-13  reduce R12: Param (|rhs|=2) → goto 20
[017] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamList E13]  ⟂ )           act=-12  reduce R11: ParamList (|rhs|=3) → goto 13
[018] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12]  ⟂ )           act=-10  reduce R9: ParamListOpt (|rhs|=1) → goto 12
[019] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16]  ⟂ )           act= 16  shift → estado 16
[020] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18]  ⟂ {           act= 18  shift → estado 18
[021] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23]  ⟂ return      act= 23  shift → estado 23
[022] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23 identificador E32]  ⟂ identificador  act= 32  shift → estado 32
[023] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23 Factor E37]  ⟂ opSuma      act=-27  reduce R26: Factor (|rhs|=1) → goto 37
[024] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23 Term E36]  ⟂ opSuma      act=-26  reduce R25: Term (|rhs|=1) → goto 36
[025] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23 Expr E35]  ⟂ opSuma      act=-25  reduce R24: Expr (|rhs|=1) → goto 35
[026] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23 Expr E35 opSuma E47]  ⟂ opSuma      act= 47  shift → estado 47
[027] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23 Expr E35 opSuma E47 identificador E32]  ⟂ identificador  act= 32  shift → estado 32
[028] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23 Expr E35 opSuma E47 Factor E37]  ⟂ ;           act=-27  reduce R26: Factor (|rhs|=1) → goto 37
[029] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23 Expr E35 opSuma E47 Term E52]  ⟂ ;           act=-26  reduce R25: Term (|rhs|=1) → goto 52
[030] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 return E23 Expr E35]  ⟂ ;           act=-24  reduce R23: Expr (|rhs|=3) → goto 35
[031] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 Return E29]  ⟂ ;           act=-23  reduce R22: Return (|rhs|=2) → goto 29
[032] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 Return E29 ; E43]  ⟂ ;           act= 43  shift → estado 43
[033] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 Stmt E27]  ⟂ }           act=-21  reduce R20: Stmt (|rhs|=2) → goto 27
[034] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26]  ⟂ }           act=-17  reduce R16: StmtList (|rhs|=1) → goto 26
[035] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtListOpt E25]  ⟂ }           act=-16  reduce R15: StmtListOpt (|rhs|=1) → goto 25
[036] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtListOpt E25 } E40]  ⟂ }           act= 40  shift → estado 40
[037] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 Block E19]  ⟂ tipo        act=-14  reduce R13: Block (|rhs|=3) → goto 19
[038] [E0 DeclList E3 FunDef E6]                                    ⟂ tipo        act= -8  reduce R7: FunDef (|rhs|=6) → goto 6
[039] [E0 DeclList E3 Decl E8]                                      ⟂ tipo        act= -6  reduce R5: Decl (|rhs|=1) → goto 8
[040] [E0 DeclList E3]                                              ⟂ tipo        act= -3  reduce R2: DeclList (|rhs|=2) → goto 3
[041] [E0 DeclList E3 tipo E1]                                      ⟂ tipo        act=  1  shift → estado 1
[042] [E0 DeclList E3 tipo E1 identificador E7]                     ⟂ identificador  act=  7  shift → estado 7
[043] [E0 DeclList E3 tipo E1 identificador E7 ( E10]               ⟂ (           act= 10  shift → estado 10
[044] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12]  ⟂ )           act= -9  reduce R8: ParamListOpt (|rhs|=0) → goto 12
[045] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16]  ⟂ )           act= 16  shift → estado 16
[046] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18]  ⟂ {           act= 18  shift → estado 18
[047] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 tipo E21]  ⟂ tipo        act= 21  shift → estado 21
[048] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 tipo E21 identificador E30]  ⟂ identificador  act= 30  shift → estado 30
[049] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 VarDecl E24]  ⟂ ;           act= -7  reduce R6: VarDecl (|rhs|=2) → goto 24
[050] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 VarDecl E24 ; E39]  ⟂ ;           act= 39  shift → estado 39
[051] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 Stmt E27]  ⟂ tipo        act=-19  reduce R18: Stmt (|rhs|=2) → goto 27
[052] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26]  ⟂ tipo        act=-17  reduce R16: StmtList (|rhs|=1) → goto 26
[053] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 tipo E21]  ⟂ tipo        act= 21  shift → estado 21
[054] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 tipo E21 identificador E30]  ⟂ identificador  act= 30  shift → estado 30
[055] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 VarDecl E24]  ⟂ ;           act= -7  reduce R6: VarDecl (|rhs|=2) → goto 24
[056] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 VarDecl E24 ; E39]  ⟂ ;           act= 39  shift → estado 39
[057] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 Stmt E41]  ⟂ tipo        act=-19  reduce R18: Stmt (|rhs|=2) → goto 41
[058] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26]  ⟂ tipo        act=-18  reduce R17: StmtList (|rhs|=2) → goto 26
[059] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 tipo E21]  ⟂ tipo        act= 21  shift → estado 21
[060] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 tipo E21 identificador E30]  ⟂ identificador  act= 30  shift → estado 30
[061] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 VarDecl E24]  ⟂ ;           act= -7  reduce R6: VarDecl (|rhs|=2) → goto 24
[062] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 VarDecl E24 ; E39]  ⟂ ;           act= 39  shift → estado 39
[063] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 Stmt E41]  ⟂ identificador  act=-19  reduce R18: Stmt (|rhs|=2) → goto 41
[064] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26]  ⟂ identificador  act=-18  reduce R17: StmtList (|rhs|=2) → goto 26
[065] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22]  ⟂ identificador  act= 22  shift → estado 22
[066] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31]  ⟂ =           act= 31  shift → estado 31
[067] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32]  ⟂ identificador  act= 32  shift → estado 32
[068] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Factor E37]  ⟂ opSuma      act=-27  reduce R26: Factor (|rhs|=1) → goto 37
[069] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Term E36]  ⟂ opSuma      act=-26  reduce R25: Term (|rhs|=1) → goto 36
[070] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Expr E44]  ⟂ opSuma      act=-25  reduce R24: Expr (|rhs|=1) → goto 44
[071] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Expr E44 opSuma E47]  ⟂ opSuma      act= 47  shift → estado 47
[072] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Expr E44 opSuma E47 identificador E32]  ⟂ identificador  act= 32  shift → estado 32
[073] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Expr E44 opSuma E47 Factor E37]  ⟂ ;           act=-27  reduce R26: Factor (|rhs|=1) → goto 37
[074] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Expr E44 opSuma E47 Term E52]  ⟂ ;           act=-26  reduce R25: Term (|rhs|=1) → goto 52
[075] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Expr E44]  ⟂ ;           act=-24  reduce R23: Expr (|rhs|=3) → goto 44
[076] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 Assign E28]  ⟂ ;           act=-22  reduce R21: Assign (|rhs|=3) → goto 28
[077] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 Assign E28 ; E42]  ⟂ ;           act= 42  shift → estado 42
[078] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 Stmt E41]  ⟂ identificador  act=-20  reduce R19: Stmt (|rhs|=2) → goto 41
[079] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26]  ⟂ identificador  act=-18  reduce R17: StmtList (|rhs|=2) → goto 26
[080] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22]  ⟂ identificador  act= 22  shift → estado 22
[081] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31]  ⟂ =           act= 31  shift → estado 31
[082] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32]  ⟂ identificador  act= 32  shift → estado 32
[083] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45]  ⟂ (           act= 45  shift → estado 45
[084] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 entero E33]  ⟂ entero      act= 33  shift → estado 33
[085] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 Factor E37]  ⟂ ,           act=-28  reduce R27: Factor (|rhs|=1) → goto 37
[086] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 Term E36]  ⟂ ,           act=-26  reduce R25: Term (|rhs|=1) → goto 36
[087] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 Expr E48]  ⟂ ,           act=-25  reduce R24: Expr (|rhs|=1) → goto 48
[088] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 ArgList E50]  ⟂ ,           act=-34  reduce R33: ArgList (|rhs|=1) → goto 50
[089] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 ArgList E50 , E54]  ⟂ ,           act= 54  shift → estado 54
[090] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 ArgList E50 , E54 entero E33]  ⟂ entero      act= 33  shift → estado 33
[091] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 ArgList E50 , E54 Factor E37]  ⟂ )           act=-28  reduce R27: Factor (|rhs|=1) → goto 37
[092] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 ArgList E50 , E54 Term E36]  ⟂ )           act=-26  reduce R25: Term (|rhs|=1) → goto 36
[093] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 ArgList E50 , E54 Expr E55]  ⟂ )           act=-25  reduce R24: Expr (|rhs|=1) → goto 55
[094] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 ArgList E50]  ⟂ )           act=-35  reduce R34: ArgList (|rhs|=3) → goto 50
[095] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 ArgListOpt E49]  ⟂ )           act=-33  reduce R32: ArgListOpt (|rhs|=1) → goto 49
[096] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 identificador E32 ( E45 ArgListOpt E49 ) E53]  ⟂ )           act= 53  shift → estado 53
[097] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Call E38]  ⟂ ;           act=-31  reduce R30: Call (|rhs|=4) → goto 38
[098] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Factor E37]  ⟂ ;           act=-30  reduce R29: Factor (|rhs|=1) → goto 37
[099] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Term E36]  ⟂ ;           act=-26  reduce R25: Term (|rhs|=1) → goto 36
[100] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 identificador E22 = E31 Expr E44]  ⟂ ;           act=-25  reduce R24: Expr (|rhs|=1) → goto 44
[101] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 Assign E28]  ⟂ ;           act=-22  reduce R21: Assign (|rhs|=3) → goto 28
[102] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 Assign E28 ; E42]  ⟂ ;           act= 42  shift → estado 42
[103] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26 Stmt E41]  ⟂ }           act=-20  reduce R19: Stmt (|rhs|=2) → goto 41
[104] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtList E26]  ⟂ }           act=-18  reduce R17: StmtList (|rhs|=2) → goto 26
[105] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtListOpt E25]  ⟂ }           act=-16  reduce R15: StmtListOpt (|rhs|=1) → goto 25
[106] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 { E18 StmtListOpt E25 } E40]  ⟂ }           act= 40  shift → estado 40
[107] [E0 DeclList E3 tipo E1 identificador E7 ( E10 ParamListOpt E12 ) E16 Block E19]  ⟂ $           act=-14  reduce R13: Block (|rhs|=3) → goto 19
[108] [E0 DeclList E3 FunDef E6]                                    ⟂ $           act= -8  reduce R7: FunDef (|rhs|=6) → goto 6
[109] [E0 DeclList E3 Decl E8]                                      ⟂ $           act= -6  reduce R5: Decl (|rhs|=1) → goto 8
[110] [E0 DeclList E3]                                              ⟂ $           act= -3  reduce R2: DeclList (|rhs|=2) → goto 3
[111] [E0 Program E2]                                               ⟂ $           act= -2  reduce R1: Program (|rhs|=1) → goto 2
[112] [E0 Program E2]                                               ⟂ $           act= -1  ACCEPT

*/
