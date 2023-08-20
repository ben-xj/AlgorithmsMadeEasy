import time
import pulp


def solve_mip_model(N,
                    M,
                    c,
                    max_day_time=6,
                    max_single_day_time=4,
                    min_cont=3,
                    min_interval=4,
                    EN=3):
    # Create a LP problem
    problem = pulp.LpProblem("Exercise_Scheduling", pulp.LpMaximize)

    # Variables
    x = [
        pulp.LpVariable(f'x_{i}', lowBound=0, upBound=500, cat=pulp.LpInteger)
        for i in range(N)
    ]
    y = [pulp.LpVariable(f'y_{i}', cat=pulp.LpBinary) for i in range(N)]
    t = [[pulp.LpVariable(f't_{i}_{j}', lowBound=0, upBound=max_day_time,
                        cat=pulp.LpInteger) for j in range(M)] 
                        for i in range(N)]
    z = [[pulp.LpVariable(f'z_{i}_{j}', cat=pulp.LpBinary) for j in range(M)]
         for i in range(N)]

    # Constraints
    for i in range(N):
        problem += x[i] == sum(t[i][j] * c[j] for j in range(M))
        problem += sum(t[i][j] for j in range(M)) <= max_day_time
        for j in range(M):
            problem += t[i][j] <= max_single_day_time
        if i <= N - min_cont - 1:
            problem += sum(y[k]
                           for k in range(i, i + min_cont + 1)) <= min_cont

        if i <= N - min_interval - 1:
            for j in range(M):
                problem += sum(z[k][j]
                               for k in range(i, i + min_interval + 1)) <= 1

        problem += sum(z[i][j] for j in range(M)) <= EN

        problem += y[i] * 500 >= x[i]
        # problem += y[i] <= x[i]

        for j in range(M):
            problem += z[i][j] * 6 >= t[i][j]
            # problem += z[i][j] <= t[i][j]

    # Objective
    objective = sum(x[i] for i in range(N))
    problem += objective

    # Solve the model
    problem.solve(pulp.CPLEX_PY(msg=False))

    # Print results
    if problem.status == pulp.LpStatusOptimal:
        print('wall time =', problem.solutionCpuTime)
        print('Objective value =', pulp.value(objective))
        # for i in range(N):
        #     print(f'Day {i + 1}: ')
        #     for j in range(M):
        #         if z[i][j].value() == 1:
        #             print(f'{exercise[j]}: {t[i][j].value() * 10}  minutes')
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    # Define your parameters here
    N = 30
    M = 6
    c = [15, 20, 30, 28, 27,
        18]  # List of consumption values for each type of exercise
    exercise = ['Push-ups', 'Sit-ups', 'Squats', 'Pull-ups', 'Leg-lifts', 'Planks']

    # time the following function call
    s = time.perf_counter()
    for i in range(10):
        solve_mip_model(N, M, c)
    e = time.perf_counter()
    print(f'Average time: {(e - s) / 10}')