Синтаксический анализатор пролога с помощью библиотеки yacc
=============================

Инструкция по сборке и запуску
------------

Программа использует библиотеку ply.

Программа принимает на вход в качестве аргумента командной строки файл 
с последовательностью определений отношений на языке пролог. Записывает результат 
работы програмы в файл с расширением **.out**

Запускать командой:

      python3 parser.py file

Примеры корректного синтаксиса
------------
    f
    . f.
    f
    .
    g f (ffdfjsh) sdas sda :- d.
    f :-
    (g, g, g, ggg g g g); sdsada (sdasd) sdsad (sdasd); sfsdf, dfsdfsd (ssdf), (sdsf; sfs; fsdf; f)
    .
    
    f (((f))) :- f (ff f).
    odd (cons H (cons H1 T)) (cons H T1) :- odd T T1.
    odd (cons H nil) nil.
    odd nil nil.
    f :- (a b) , (c d).
    f (cons h t) :- g h, f t.
    f :- g, ((h); t).
    f :- g, (h; t).
    f.
    f :- g.
    f :- g. f :- g.
    f :- g, h; t.
    f :- g, (h; t).
    f a :- g, h (t c d).
    f (cons h t) :- g h, f t.
    f (f).
    f f f f f f.
    f (f) (f) (f).
    f f (f (f (f (f f)))).
    f f (f f) f.
    f (f f) (f f) f
    f :- g, ((h); t).
    f :- g, (h; t).
    odd (cons H (cons H1 T)) (cons H T1) :- odd T T1.
    odd (cons H nil) nil.
    odd nil nil.
    f :- (a b) , (c d).
    f (cons h t) :- g h, f t.


