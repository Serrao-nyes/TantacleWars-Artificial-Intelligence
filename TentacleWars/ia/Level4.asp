color(green, 47, 171, 51).
color(red, 200, 0, 0).
color(gray, 55, 55, 55).
color(white, 255, 255, 255).
color(warmYellow, 255, 255, 85).

element_in_avgDelta(Indice, Elemento) :- avgDelta_Fact(Indice, Elemento).

Cell(300,300,0,red,0,"ATT","Defense",0,False,0,False)
Cell(150,600,15,red,0,"ATT","Defense",0,False,0,False)
Cell(230,125,10,green,0,"EMB","Defense",0,False,0,False)
Cell(450,185,15,red,0,"ATT","Defense",0,False,0,False)
Cell(560,500,10,red,0,"ATT","Defense",0,False,0,False)

% Definizione della posizione target
target_position(X, Y).

% Definizione della lunghezza dell'unità di catena (dot)
chain_unit_length(3).

% Calcolo della distanza euclidea tra una cella e la posizione target
distance(CellX, CellY, TargetX, TargetY, Distance) :-
    cell(CellX, CellY, _, _, _, _, _, _, _, _, _),
    target_position(TargetX, TargetY),
    Distance = sqrt((CellX-TargetX)**2 + (CellY-TargetY)**2).

% Conversione della distanza in unità di catena
distance_in_chain_units(CellX, CellY, TargetX, TargetY, ChainUnits) :-
    chain_unit_length(UnitLength),
    distance(CellX, CellY, TargetX, TargetY, Distance),
    DotNumber = Distance / (UnitLength * 2), % Calcolo del numero di punti (diametro = 2 * lunghezza unità di catena)
    ChainUnits = DotNumber / 2.




