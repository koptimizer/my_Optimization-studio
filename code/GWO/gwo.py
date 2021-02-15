def GWO(lb, ub, dim, searchAgents_no, maxIters):
    # Grey wolves 초기화
    alpha_pos = np.zeros(dim) # The best search agent
    alpha_score = float("inf")

    beta_pos = np.zeros(dim) # The second best search agent
    beta_score = float("inf")

    delta_pos = np.zeros(dim) # The third best search agent
    delta_score = float("inf")

    # 모든 wolf 들의 위치 랜덤 초기화 [lb, ub]
    positions = np.zeros((searchAgents_no, dim))
    for i in range(dim):
        positions[:, i] = (np.random.uniform(lb, ub, searchAgents_no))

    # Main loop
    for l in range(0, maxIters):

        # 모든 늑대들의 계층을 결정하는 Step
        for i in range(0, searchAgents_no):

            # Boundary를 벗어나는 위치 변환
            for j in range(dim):
                positions[i, j] = np.clip(positions[i, j], lb, ub)

            # i번째 wolf의 fitness 산출
            fitness = F9(positions[i, :])

            # 알파, 베타, 델타 늑대 업데이트
            # 알파 늑대보다 좋은 늑대가 나타나면 그 늑대의 fitness와 pos를 알파로 위임. 알파, 베타, 델타 늑대를 한 단계씩 강등
            if fitness < alpha_score:
                delta_score = beta_score  # Update delta
                delta_pos = beta_pos.copy()
                beta_score = alpha_score  # Update beta
                beta_pos = alpha_pos.copy()
                alpha_score = fitness  # Update alpha
                alpha_pos = positions[i, :].copy()

            # 베타 늑대 적임자가 나타나면 그 늑대의 fitness와 pos를 베타로 위임. 베타, 델타 늑대를 한 단계씩 강등
            if fitness > alpha_score and fitness < beta_score:
                delta_score = beta_score  # Update delte
                delta_pos = beta_pos.copy()
                beta_score = fitness  # Update beta
                beta_pos = positions[i, :].copy()

            # 델타 늑대 적임자가 나타나면 그 늑대의 fitness와 pos를 델타로 위임. 델타 늑대를 한 단계 강등
            if fitness > alpha_score and fitness > beta_score and fitness < delta_score:
                delta_score = fitness  # Update delta
                delta_pos = positions[i, :].copy()

        # a는 선형적으로 감소하는 값으로 2 ~ 0을 가짐
        a = 2 - l * ((2) / maxIters)

        # 모든 늑대들의 pos를 업데이트하는 Step
        for i in range(0, searchAgents_no):
            for j in range(0, dim):
                r1 = random.random()  # r1 is a random number in [0,1]
                r2 = random.random()  # r2 is a random number in [0,1]
                A1 = 2 * a * r1 - a  # Equation (3.3)
                C1 = 2 * r2  # Equation (3.4)
                D_alpha = abs(C1 * alpha_pos[j] - positions[i, j])  # Equation (3.5)-part 1
                X1 = alpha_pos[j] - A1 * D_alpha  # Equation (3.6)-part 1

                r1 = random.random()
                r2 = random.random()
                A2 = 2 * a * r1 - a  # Equation (3.3)
                C2 = 2 * r2  # Equation (3.4)
                D_beta = abs(C2 * beta_pos[j] - positions[i, j])  # Equation (3.5)-part 2
                X2 = beta_pos[j] - A2 * D_beta  # Equation (3.6)-part 2

                r1 = random.random()
                r2 = random.random()
                A3 = 2 * a * r1 - a  # Equation (3.3)
                C3 = 2 * r2  # Equation (3.4)
                D_delta = abs(C3 * delta_pos[j] - positions[i, j])  # Equation (3.5)-part 3
                X3 = delta_pos[j] - A3 * D_delta  # Equation (3.5)-part 3

                positions[i, j] = (X1 + X2 + X3) / 3  # Equation (3.7)
        print(l, "번째 최적 해 :", alpha_score)
    return "GWO :"+str(alpha_score)
