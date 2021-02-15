# 👨‍💻 My Optimization-Studio
- <b>Simulation, Metaheuristics, Optimization method, Reinforcement learning</b>
- <b>New metaheuristic algorithm</b>
  - [Recursive Fractal Search]() 
- <b>Industrial application of AI</b>
- <b>Visual simulator of process</b>
- <img src = "https://img.shields.io/badge/Language-python-blue">
<br/>

## Simulation
- <b>Job-shop Simulator</b>
  - [Single machine sequence](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/SM/sms.py)<br/>
## Metaheuristics
- <b>Genetic Algorithm</b>
  - [Find the largest number](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GA/GA_largestNumberFinder.py)<br/>
  - [Continuous problem](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GA/geneticAlgorithmOnCon.py)
  - [TSP(Traveling Salesman Problem)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GA/GA_TSP.py)<br/>
  - [TSP(Traveling Salesman Problem + Visualization)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GA/geneticAlgorithmOnDis.py)
  - [TSP(Traveling Salesman Problem + Visualization) 2](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GA/geneticAlgorithmOnDis2.py)
  - [IB Park's problem](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GA/GA_Park.py)
  - [Scheduling](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GA/geneticAlgorithmOnSch.py)
- <b>Mimitic Genetic Algorithm</b>
  - [TSP(Traveling Salesman Problem)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GA/mGA_2opt_numpyGA_2.py)<br/>
- <b>Particle Swarm Optimization</b>
  - [Continuous problem](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/PSO/PSO.py)
- <b>Cuckoo Search</b>
  - [Continuous problem](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/CS/cuckooSearchOnCon.py)
  - [Continuous problem + Visualization](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/CS/cuckooSearchOnCon2.py)
  - [TSP(Traveling Salesman Problem)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/CS/CS.py)<br/>
- <b>Improved Cuckoo Search</b>
  - [TSP(Traveling Salesman Problem)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/CS/ICS.py)<br/>
  - [TSP(Traveling Salesman Problem + Visualization)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/CS/cuckooSearchOnDis.py)
  - [Flexible Job Shop Problem](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/CS/cps2.py)
- <b>Gray Wolf Optimizer</b>
  - [Continuous problem](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GWO/gwo.py)
- <b>Recurcive Fractal Search [[about]]()</b>
  - [TSP(Traveling Salesman Problem)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/RFS/recursiveFractalSearch.py)
- <b>Industrial Application</b>
  - [NS SHOP+ 최적의 취급액을 가지는 방송편성표 탐색(CS)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/CS/nsScheduler2.py)
  - [ESWA - An effective GA for the FJSP(GA)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/GA/eswa3.py) [[논문보기]](https://github.com/koptimizer/my_PaperLog/issues/10)<br/>

## Reinforcement Learning
- <b>Q-learning</b>
  - [IB Park's Problem(Q-table)](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/RL/q_table.py)
    > A = {0,1}, len(S) = 6 <br/>
    if currentState == 01010 and action == 0 : return reward+1000 </br>
    elif a==0 : return reward+1 </br>
    elif a==1 : return reward-1 </br>
- <b>Deep Q-Networks</b>
  - [CartPole]()
  - [Flow shop Scheduling]()

## Test Function for Optimization
- Tester Module 1
  - <b>Sphere function</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/Sphere%20function.jpg">
  - <b>Rosenbrock function</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/Rosenbrock%20function.jpg">
  - <b>Rastrigin function function</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/Rastrigin%20function.jpg">
- [Tester Module 2](https://github.com/koptimizer/my_Optimization-studio/blob/master/code/simul/mySimul2.py)
  - <b>Booth function</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/Booth%20function.jpg">
  - <b>Matyas function</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/Matyas%20function.jpg">
  - <b>Ackley function</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/ackley%20function.jpg">
  - <b>Le'vi function N.13</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/levi13%20function.jpg">
  - <b>Himmelblau's function</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/himmerlblau's%20function.jpg">
  - <b>Beale function</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/Beale%20function.jpg">
  - <b>Goldstein-Price function</b>
    > <img src = "https://github.com/koptimizer/my_Optimization-studio/blob/master/pics/Goldstein-Price%20function.jpg">
