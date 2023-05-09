# %%
import sympy
from sympy import latex, pprint
# %%
"""
J = projective_transform_jacobian
T = T_camera_world
R = rotation_matrix_from_quaternion(self.cov_rotation)
S = self.cov_scale
Sigma = R @ S.outer_product(S) @ R.transpose()

homogeneous_translation_camera = T_camera_world @ ti.math.vec4(self.translation.x, self.translation.y, self.translation.z, 1)
translation_camera = ti.math.vec3(homogeneous_translation_camera.x, homogeneous_translation_camera.y, homogeneous_translation_camera.z)
uv1 = (projective_transform @ translation_camera) / translation_camera.z
uv = ti.math.vec2(uv1.x, uv1.y)
"""
"""
T is 4x4
projective_transform is 3x3
get Jacobian of D(uv)/D(translation)
"""
# %%
projective_transform = sympy.MatrixSymbol('K', 3, 3)
translation_camera = sympy.MatrixSymbol('t', 3, 1)
uv1 = (projective_transform @ translation_camera) / translation_camera[2, 0]
uv = sympy.Matrix([uv1[0, 0], uv1[1, 0]])
D_uv_D_translation_camera = uv.jacobian(translation_camera)
D_uv_D_translation_camera.simplify()
print(latex(D_uv_D_translation_camera))
pprint(D_uv_D_translation_camera, use_unicode=True)
# %%
T = sympy.MatrixSymbol('T', 4, 4)
translation = sympy.MatrixSymbol('t', 3, 1)
homogeneous_translation_camera = T @ sympy.Matrix([translation[0, 0], translation[1, 0], translation[2, 0], 1])
translation_camera = sympy.Matrix([homogeneous_translation_camera[0, 0], homogeneous_translation_camera[1, 0], homogeneous_translation_camera[2, 0]])

D_translation_camrea_D_translation = translation_camera.jacobian(translation)
D_translation_camrea_D_translation.simplify()
print(latex(D_translation_camrea_D_translation))
pprint(D_translation_camrea_D_translation, use_unicode=True)

# %%

uv1 = (projective_transform @ translation_camera) / translation_camera[2, 0]
uv = sympy.Matrix([uv1[0, 0], uv1[1, 0]])




D_uv_D_translation = uv.jacobian(translation)
D_uv_D_translation.simplify()
print(latex(D_uv_D_translation))
pprint(D_uv_D_translation, use_unicode=True)
# %%
"""
U = J @ W # 2x3
cov_uv = U @ Sigma @ U.transpose() # equation (5) in the paper
"""
U = sympy.MatrixSymbol('U', 2, 3)
Sigma = sympy.MatrixSymbol('Sigma', 3, 3)
Sigma_vec = sympy.Matrix([[Sigma[i, j]] for i in range(3) for j in range(3)])
cov_uv = U @ Sigma @ U.transpose()
cov_uv_vec = sympy.Matrix([[cov_uv[i, j]] for i in range(2) for j in range(2)])
D_cov_uv_D_U = cov_uv_vec.jacobian(Sigma_vec)
print(D_cov_uv_D_U.shape)
print(latex(D_cov_uv_D_U))
pprint(D_cov_uv_D_U, use_unicode=True)


# %%
"""
Sigma = M @ M.transpose() # covariance matrix, 3x3, equation (6) in the paper
"""
"""
M = sympy.MatrixSymbol('M', 3, 3)
Sigma = M @ M.transpose()
D_Sigma_D_M = Sigma.diff(M).as_explicit()
print(D_Sigma_D_M.shape)
print(latex(D_Sigma_D_M))
pprint(D_Sigma_D_M, use_unicode=True)
"""
M = sympy.Matrix([[sympy.Symbol(f"m{i}{j}") for j in range(3)] for i in range(3)])
M_vector = sympy.Matrix([[M[i, j]] for i in range(3) for j in range(3)])

Sigma = M @ M.transpose()
Sigma_vector = sympy.Matrix([[Sigma[i, j]] for i in range(3) for j in range(3)])
D_Sigma_D_M = Sigma_vector.jacobian(M_vector)
print(D_Sigma_D_M.shape)
print(latex(D_Sigma_D_M))
pprint(D_Sigma_D_M, use_unicode=True)
# %%
# M = R @ S
R = sympy.MatrixSymbol('R', 3, 3)
S = sympy.Matrix([
    [sympy.Symbol("s00"), 0, 0],  
    [0, sympy.Symbol("s11"), 0],
    [0, 0, sympy.Symbol("s22")]
])
s_vec = sympy.Matrix([S[i, i] for i in range(3)])
M = R @ S
M_vector = sympy.Matrix([[M[i, j]] for i in range(3) for j in range(3)])
D_M_D_s = M_vector.jacobian(s_vec)
print(D_M_D_s.shape)
print(latex(D_M_D_s))
pprint(D_M_D_s, use_unicode=True)
# %%
"""

@ti.func
def rotation_matrix_from_quaternion(q: ti.math.vec4) -> ti.math.mat3:
    xx = q.x * q.x
    yy = q.y * q.y
    zz = q.z * q.z
    xy = q.x * q.y
    xz = q.x * q.z
    yz = q.y * q.z
    wx = q.w * q.x
    wy = q.w * q.y
    wz = q.w * q.z
    return ti.math.mat3([
        [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
        [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
        [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)]
    ])
 
"""
x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')
w = sympy.Symbol('w')
xx = x * x
yy = y * y
zz = z * z
xy = x * y
xz = x * z
yz = y * z
wx = w * x
wy = w * y
wz = w * z
q = sympy.Matrix([[x], [y], [z], [w]])
R = sympy.Matrix([
    [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
    [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
    [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)]
])
S = sympy.Matrix([
    [sympy.Symbol("s00"), 0, 0],  
    [0, sympy.Symbol("s11"), 0],
    [0, 0, sympy.Symbol("s22")]
])
M = R @ S
M_vector = sympy.Matrix([[M[i, j]] for i in range(3) for j in range(3)])
d_M_d_q = M_vector.jacobian(q)
print(d_M_d_q.shape)
print(latex(d_M_d_q))
pprint(d_M_d_q, use_unicode=True)

# %%
R = sympy.MatrixSymbol('R', 3, 3)
S = sympy.Matrix([
    [sympy.Symbol("s00"), 0, 0],  
    [0, sympy.Symbol("s11"), 0],
    [0, 0, sympy.Symbol("s22")]
])
Sigma = R @ S @ S.transpose() @ R.transpose()
pprint(Sigma.as_explicit(), use_unicode=True)
# %%
R = sympy.MatrixSymbol('R', 3, 3)
S = sympy.MatrixSymbol('S', 3, 1)
Sigma = R @ S @ S.transpose() @ R.transpose()
pprint(Sigma.as_explicit(), use_unicode=True)
#
# %%
import sympy
from sympy import latex, pprint
J = sympy.MatrixSymbol('J', 2, 3)
T = sympy.MatrixSymbol('T', 4, 4)
cx = sympy.Symbol('cx')
cy = sympy.Symbol('cy')
cz = sympy.Symbol('cz')
cw = sympy.Symbol('cw')

cov = sympy.Matrix([cx, cy, cz, cw])
R = sympy.Matrix([
    [1 - 2 * (cy * cy + cz * cz), 2 * (cx * cy - cw * cz), 2 * (cx * cz + cw * cy)],
    [2 * (cx * cy + cw * cz), 1 - 2 * (cx * cx + cz * cz), 2 * (cy * cz - cw * cx)],
    [2 * (cx * cz - cw * cy), 2 * (cy * cz + cw * cx), 1 - 2 * (cx * cx + cy * cy)]
])
tx = sympy.Symbol('tx')
ty = sympy.Symbol('ty')
tz = sympy.Symbol('tz')
translation = sympy.Matrix([tx, ty, tz])
sx = sympy.Symbol('sx')
sy = sympy.Symbol('sy')
sz = sympy.Symbol('sz')
s = sympy.Matrix([sx, sy, sz])
S = sympy.Matrix([
    [s[0, 0], 0, 0],  
    [0, s[1, 0], 0],
    [0, 0, s[2, 0]]
])
Sigma = R @ S @ S.transpose() @ R.transpose()
homogeneous_translation_camera = T @ sympy.Matrix([translation[0, 0], translation[1, 0], translation[2, 0], 1])
translation_camera = sympy.Matrix([homogeneous_translation_camera[0, 0], homogeneous_translation_camera[1, 0], homogeneous_translation_camera[2, 0]])
uv1 = (J @ translation_camera) / translation_camera[2, 0]
uv = sympy.Matrix([uv1[0, 0], uv1[1, 0]])
W = T[:3, :3]
cov_uv = J @ W @ Sigma @ W.transpose() @ J.transpose()
cov_uv_vec = sympy.Matrix([cov_uv[0, 0], cov_uv[0, 1], cov_uv[1, 0], cov_uv[1, 1]])
J_cov_uv_cov = cov_uv_vec.jacobian(cov)
print(J_cov_uv_cov.shape)
print(sympy.python(J_cov_uv_cov))
J_cov_uv_s = cov_uv_vec.jacobian(s)
print(J_cov_uv_s.shape)
print(sympy.python(J_cov_uv_s))
J_uv_translation = uv.jacobian(translation)
print(J_uv_translation.shape)
print(sympy.python(J_uv_translation))
# %%
fx = sympy.Symbol('fx')
fy = sympy.Symbol('fy')
cx = sympy.Symbol('cx')
cy = sympy.Symbol('cy')
x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')
K = sympy.Matrix([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
])
uv1 = K @ sympy.Matrix([[x], [y], [z]]) / z
uv = sympy.Matrix([uv1[0, 0], uv1[1, 0]])
J = uv.jacobian(sympy.Matrix([[x], [y], [z]]))
print(J.shape)
print(sympy.python(J))

# %%