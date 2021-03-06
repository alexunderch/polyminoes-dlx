# polyminoes-dlx
Python package to determine whether polyminoes can fill a given grid.

## Project description:
[Проблема](ttps://en.wikipedia.org/wiki/Set_cover_problem), которая поставлена -- NP-полная, как задача о рюкзаке, то есть сводима к ней за полиномиальное время.

Я поставил данную задачу как задачу покрытия множества, для которой можно использовать приближённые решения типа _SAT-solver_'a, основанного на КНФ или различных дереьев поиска -- ограничений полного перебора: бинарный поиск, жадный алгоритм, метод ветвей и границ, различные алгоритмы поиска по графам, ведь данную задачу можно представить на задачу покрытия максимыльного количества вершин клетчатой решётки заданным фигурками-полимино.

Но для данной задачи я решил пойти по другому пути: использовать найденную по теме [статью](https://arxiv.org/abs/cs/0011047) Дональда Кнута о простейшем алгоритме <<проб и ошибок>> (DFS), но который с введёнными модификацими решениями [делает](https://www.quora.com/What-is-the-space-and-time-complexity-of-Donald-Knuths-algorithm-X-implemented-using-dancing-links) задачу за O($2^(2n/5)$), но в реальности O($2^(n/3)$) за счёт выбора точки покрытия.
По памяти у него расход -- O($n^2$), что не так уж и плохо.

Дополнительные расходы свзяаны с интерпретацией задачи -- так как замощение может быть неполным, то я ввёл концепцию незаполненных клеток, _holes_, чтобы получать точное решение максимально быстро.

За описанием каждой полиминошки -- см. код.

P.s. костыль: у меня реализовано двоякое представление полиномино: координатное, чтобы удобно поворачивать и двигать фигурки, и нумерованное по клеткам заполнения, для алгоритма X, но оно не хранится, а просто тратится линейное время для перехода из одного в другое.

