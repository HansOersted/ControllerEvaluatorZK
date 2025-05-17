import numpy as np
import matplotlib.pyplot as plt

# load A from stability_proof output
model_data = np.load('final_model_weights.npz')
A = model_data['A']

# load training data from interested_section output
data = np.load('interested_section_output.npz')
e_interested = data['interested_TrackingError']
de_interested = data['interested_der_interested_TrackingError']
dde_interested = data['der_der_interested_TrackingError']

# reshape and prepare data
lambda_val = 0.0009

E_interested = np.stack((de_interested, dde_interested), axis=1)

constraint_values = []
for row in E_interested:
    de = np.array([[row[0]], [row[1]]])
    dde = np.array([[row[1]], [0]])
    c = (dde.T @ A @ de + de.T @ A @ dde + lambda_val * de.T @ A @ de).item()
    constraint_values.append(c)

# plot constraints
plt.figure()
plt.plot(range(len(constraint_values)), constraint_values, linewidth=2)
plt.xlabel('Training Sample Index')
plt.ylabel('Constraint Value')
plt.title('Constraints from Training Data')
plt.grid(True)
plt.savefig('training_constraint_curve.png')
plt.close()

print("✅ Constraint plot saved as training_constraint_curve.png")
print(f"🔍 Max constraint value: {max(constraint_values):.6f}")