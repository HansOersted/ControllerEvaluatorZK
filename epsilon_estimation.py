import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# load previously trained A from stability_proof output
model_data = np.load('final_model_weights.npz')
A = model_data['A']

# training config
n_training = 2
lambda_val = 5
sample_time = 0.002

# load CSV data
df = pd.read_csv('final_data.csv')

time = df['timestamp'].to_numpy()
q_ref_first = df['target_q_3'].to_numpy()
dq_ref_first = df['target_qd_3'].to_numpy()
q_ref_second = df['target_q_5'].to_numpy()
dq_ref_second = df['target_qd_5'].to_numpy()

q_actual_first = df['actual_q_3'].to_numpy()
dq_actual_first = df['actual_qd_3'].to_numpy()
q_actual_second = df['actual_q_5'].to_numpy()
dq_actual_second = df['actual_qd_5'].to_numpy()

e_csv_first = q_actual_first - q_ref_first
de_csv_first = dq_actual_first - dq_ref_first
e_csv_second = q_actual_second - q_ref_second
de_csv_second = dq_actual_second - dq_ref_second

dde_csv_first = np.diff(e_csv_first) / sample_time
dde_csv_second = np.diff(e_csv_second) / sample_time

# valid nontrivial indices
nontrival_idx = np.array([...])  # ← Fill in with your full 99x2 index array

# collect training index
training_index = []
for i in range(n_training):
    training_index.extend(range(nontrival_idx[i, 0], nontrival_idx[i, 1] + 1))
training_index = np.array(training_index)

# collect training data (only 1st derivative, consistent with stability_proof)
de_training_first = de_csv_first[training_index]
de_training_second = de_csv_second[training_index]
dde_training_first = dde_csv_first[training_index]
dde_training_second = dde_csv_second[training_index]

de_training = np.stack((de_training_first, de_training_second), axis=1)
dde_training = np.stack((dde_training_first, dde_training_second), axis=1)

# compute constraints
constraint_values = []
for de, dde in zip(de_training, dde_training):
    de = de.reshape(-1, 1)
    dde = dde.reshape(-1, 1)
    c = dde.T @ A @ de + de.T @ A @ dde + lambda_val * de.T @ A @ de
    constraint_values.append(c.item())

# plot constraints
plt.figure()
plt.plot(range(len(constraint_values)), constraint_values, linewidth=2)
plt.xlabel('Training Sample Index')
plt.ylabel('Constraint Value')
plt.title('Constraints from Training Data')
plt.grid(True)
plt.savefig('training_constraint_curve.png')
plt.close()
