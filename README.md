# Ising Model Visualization
## Description of the Simulation
There exists a large field of spins ($N$ of them), any of which can be either spin up (+1) or spin down (-1): $S_i \in \{-1, +1\}$. The Hamiltonian for these spins can be expressed as a function of their interactions. For example

$$
    \mathcal{H} = -\frac{J}{2} \sum_{i=1}^{N} \sum_{j} ' S_i S_j - H \sum_{i=1}^{N} S_i
$$

for interactions with nearest neighbours only (the prime denotes summation over nearest neighbours), where we set the external field $H$ to zero for the moment. Since the number of spins is constant, the volume is constant (the spins don't move), and the temperature is held constant, we know that we are in an (N, V, T) (or canonical) emsemble. Hence the partition function for any one spin is

$$
    Z_1 = \sum_{S_1} e^{-\beta U_i} = e^{\beta U_i} + e^{-\beta U_i}
$$

where $U_i = -\frac{J}{2} S_i \sum_{j} ' S_j$ and $S_i$ is spin $i$. From this we can calculate the probability that spin $i$ will be up or down from the temperature $T$ and the current state of its nearest neighbours. This is what we will use to run the simulation, e.g. at every timestep we determine the probabilities for every spin to be up or down (using equation (2)), and then update all the spins in one go.

## Theoretical Predictions
If we let $S_i = \langle S \rangle + \delta_i$ and apply a mean-field approximation (i.e. $\delta_i \delta_j = 0$ in this case) we arrive, after plenty of math, at the mean-field Hamiltonian

$$
    \mathcal{H}_{MF} \approx \frac{JNz}{2} \langle S \rangle ^2 - J z \langle S \rangle \sum_{i=1}^{N} S_i
$$

where $N$ is the number of spins, $z$ is the number of nearest neighbours of each spin (2 in 1D, 4 in 2D, etc.), and $\langle S \rangle$ is the mean spin. Noting that the total (approximate) partition function of the system is

$$
    Z_{MF} = \sum_{S_1} \dotsb \sum_{S_N} e^{-\beta \mathcal{H}_{MF}}
$$

we can calculate the average of spin $i$ to be

$$
    \langle S_i \rangle = \sum_{S_1} \dotsb \sum_{S_N} S_i \frac{e^{-\beta \mathcal{H}_{MF}}}{Z_{MF}} = \frac{\sum_{S_1} \dotsb \sum_{S_N} S_i e^{-\beta \mathcal{H}_{MF}}}{\sum_{S_1} \dotsb \sum_{S_N} e^{-\beta \mathcal{H}_{MF}}} = \frac{\sum_{S_i} S_i e^{\beta J z \langle S \rangle S_i}}{\sum_{S_i} e^{\beta J z \langle S \rangle S_i}} = \tanh{(\beta J z \langle S \rangle)}
$$

where we have cancelled the factor $e^{\frac{J N z}{2} \langle S \rangle ^2}$ on the top and bottom, we have also cancelled all the sums which do not depend on $S_i$, since they will all be equal. Since all spins are similar and we have introduced no asymmetries into the system, we define $m \equiv \langle S_i \rangle = \langle S \rangle$, and equation (5) becomes

$$
    m = \tanh{(\beta J z m)}
$$

This equation can be solved graphically to yield a single solution ($m=0$) if $\frac{1}{\beta J z} \geq 1$ and three solutions ($m=0$ and $m=\pm m_f$) if $\frac{1}{\beta J z} < 1$. It can be shown that the $m=\pm m_f$ solutions have a lower free energy. Since $m=0$ indicates a disordered state (e.g. equal numbers of up- and down spins) and $m=\pm m_f$ indicates a more ordered state (e.g. more spins up (for $m=m_f$) or more spins down (for $m=-m_f$)), we expect a phase transition at $T_c k_B = J z$.

## Goal
In this project we will try to verify that this phase transition actually happens at the specified temperature.

## Future Goals
As future aspirations we will try to graphically visualize the average spin as a function of temperature. At some point we will also attempt to introduce an external field and determine how this changes the behaviour of the simulation. In particular, we are interested in seeing if the simulation "collapses" to a majority spin-up or spin-down as a result of the external field.

## Results
The figure below shows the results from the simulation using only nearest neighbour interactions, where the coupling constant between some spin and its nearest neighbours $J=1$, and the Boltzmann constant $k_B = 1$.

![Nearest Neighbour Interactions](markdown/nearest_neighbour_graph.png)

Since this is a 2D simulation, the number of nearest neighbours $z = 4$ and thus we expect a phase transition at a critical temperature of $T_c = \frac{Jz}{k_B} = z = 4$. We do observe this in the theoretical predictions. However, the simulation results indicate the phase transition is not as abrupt as theory predicts. We argue this is a result of the mean-field approximation we used to find the theoretical predictions.

An interesting observation is the fact that the simulation always seems to collapse to positive average spin. The simulation collapses to negative average spin when the coupling constant is negative. We only take the positive solution ($m=+m_f$) in the theoretical prediction because we use a positive coupling constant, the negative solution ($m=-m_f$) is ignored.
