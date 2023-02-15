is_member(X,[X|_]).
is_member(X,[_|T]) :- is_member(X,T).

remove_duplicate([],[]).
remove_duplicate([H|T],[H|Out]) :-not(is_member(H,T)), remove_duplicate(T,Out).
remove_duplicate([H|T],Out) :- is_member(H,T), remove_duplicate(T,Out). 