from functions import *

T0 = 300.0
P0 = 101325.0
Phi = [0.5, 1, 2, 3, 4] 


tempForDifferentPressures("HP", T0)
tempForDifferentPressures("SV", T0)

tempForDifferentInitTemp("HP", P0)
tempForDifferentInitTemp("SV", P0)

for phi in Phi: tempForPhi(phi, "HP")

for phi in Phi: tempForPhi(phi, "SV")



#plt.show()