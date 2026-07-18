---
title: "From four equilibrium equations to one: faster pure-CO₂ depressurization"
description: "How the saturation curve reduces the pure-component UV flash, how differentiating the constraint yields a temperature ODE, and where the efficiency–conservation trade-off appears."
published: 2026-07-18T09:00:00+02:00
draft: false
tags:
  - phase equilibrium
  - CO₂ depressurization
  - differential-algebraic equations
  - finite volume methods
---

During a CO₂ pipeline depressurization, a finite-volume solver advances density, momentum, and total energy. It does **not** directly advance temperature or vapour fraction. These must be reconstructed from thermodynamics, often by solving a nonlinear equilibrium problem in every cell and at every time step.

For pure CO₂, that standard calculation can be simplified dramatically. The key geometric fact is that vapour–liquid equilibrium has only one thermodynamic degree of freedom: all equilibrium states lie on the saturation curve. This article explains how that fact reduces the full equilibrium problem to one scalar equation, and then goes one step further by turning the constraint into a temperature evolution equation.

The work was published as *A new temperature evolution equation that enforces thermodynamic vapour–liquid equilibrium in multiphase flows – application to CO₂ modelling* in **Computers & Fluids**. A local copy is available [here](../../articles/NewTemperatureEquation.pdf).

## Why the usual closure is expensive

For a pure fluid in two-phase equilibrium, suppose the flow solver provides mixture density $\tilde\rho$ and mixture specific internal energy $\tilde e$. A direct formulation solves for four unknowns:

$$
\alpha_g,\qquad \rho_g,\qquad \rho_\ell,\qquad T,
$$

where $\alpha_g$ is vapour volume fraction and $\rho_g$, $\rho_\ell$ are the phase densities. The equations impose mixture mass and energy together with equality of phase pressure and Gibbs free energy:

$$
\begin{aligned}
\alpha_g\rho_g+(1-\alpha_g)\rho_\ell &= \tilde\rho,\\
\alpha_g\rho_g e_g+(1-\alpha_g)\rho_\ell e_\ell &= \tilde\rho\tilde e,\\
p(\rho_g,T)&=p(\rho_\ell,T),\\
G(\rho_g,T)&=G(\rho_\ell,T).
\end{aligned}
$$

This is a UV-type flash written in density variables. It is physically direct, but solving four coupled nonlinear equations thousands of times per step is expensive, particularly with a detailed Helmholtz-energy equation of state such as Span–Wagner.

## The saturation curve removes three unknowns

Along the pure-component saturation curve, temperature determines the coexisting pressure, phase densities, and phase energies:

$$
p=p_{\mathrm{sat}}(T),\quad
\rho_g=\rho_g(T),\quad
\rho_\ell=\rho_\ell(T),\quad
e_g=e(\rho_g(T),T),\quad
e_\ell=e(\rho_\ell(T),T).
$$

Pressure equality and Gibbs-energy equality are already encoded in these saturation relations. For a specified mixture density, the volume fraction follows explicitly from the lever rule:

$$
\alpha_g(T)=\frac{\rho_\ell(T)-\tilde\rho}
{\rho_\ell(T)-\rho_g(T)}.
$$

Substituting this expression into the mixture-energy equation leaves only one unknown, $T$. Define

$$
\psi_g(\rho,T)=
\frac{\rho_\ell(T)-\rho}{\rho_\ell(T)-\rho_g(T)}
\rho_g(T)e_g(T),
$$

$$
\psi_\ell(\rho,T)=
\frac{\rho-\rho_g(T)}{\rho_\ell(T)-\rho_g(T)}
\rho_\ell(T)e_\ell(T).
$$

Then the two-phase closure is the scalar equation

$$
\psi_g(\tilde\rho,T)+\psi_\ell(\tilde\rho,T)=\tilde\rho\tilde e.
$$

In a single phase, the same notation can be extended with $\psi(\rho,T)=\rho e(\rho,T)$. The closure therefore becomes

$$
\psi(\rho,T)=\rho e
$$

in both regimes, with a piecewise definition of $\psi$. I call this the **Reduced-VLE-Algebraic** formulation. It replaces a four-unknown nonlinear system by a one-dimensional root solve.

<aside class="key-point"><strong>Why this reduction is special to a pure component</strong><br />A multicomponent two-phase mixture occupies a finite phase envelope and retains compositional degrees of freedom. Temperature alone cannot determine the phase split. The reduction is powerful precisely because pure-fluid vapour–liquid equilibrium lies on a one-dimensional saturation curve.</aside>

## From an algebraic constraint to a temperature equation

The scalar equation is already cheaper, but it still requires a nonlinear solve. The next idea starts from the fact that the flash is embedded in a time-dependent simulation. Density, energy, and temperature are functions of time, so differentiate the equilibrium identity:

$$
\frac{\partial\psi}{\partial\rho}\frac{d\rho}{dt}
+
\frac{\partial\psi}{\partial T}\frac{dT}{dt}
=
\frac{d(\rho e)}{dt}.
$$

Solving for the temperature derivative gives

$$
\boxed{
\frac{dT}{dt}=
\left[
\frac{d(\rho e)}{dt}
-
\left(\frac{\partial\psi}{\partial\rho}\right)_T
\frac{d\rho}{dt}
\right]
\bigg/
\left(\frac{\partial\psi}{\partial T}\right)_\rho
}
$$

This is the **Reduced-VLE-ODE** formulation. If the initial condition satisfies the equilibrium constraint and the differential equation is integrated exactly, the trajectory remains on the equilibrium manifold. Numerically, the method evolves temperature together with the flow variables and avoids a dedicated nonlinear flash solve.

## Coupling the equation to a finite-volume pipe model

For a pipe cell, the conservative semi-discrete equations supply

$$
\frac{d\rho}{dt}=f_1,\qquad
\frac{d(\rho u)}{dt}=f_2,\qquad
\frac{d(\rho E)}{dt}=f_3,
$$

where the $f_i$ are the finite-volume flux residuals. Since

$$
\rho e=\rho E-\frac{1}{2}\rho u^2,
$$

the internal-energy rate can be assembled from the three conservative rates. The resulting cellwise temperature equation is

$$
\frac{dT}{dt}=
\left[
f_3-u f_2+\frac{1}{2}u^2 f_1
-
\left(\frac{\partial\psi}{\partial\rho}\right)_T f_1
\right]
\bigg/
\left(\frac{\partial\psi}{\partial T}\right)_\rho.
$$

The important implementation detail is that the pressure used in the flux still comes from the same thermodynamic state. The method is not “fluid dynamics first, temperature correction later.” Temperature is part of the coupled ODE state and affects the flux at each stage.

For a tank, the same construction is even clearer. Mass and energy balances provide $d\rho/dt$ and $d(\rho e)/dt$ from inlet/outlet flow and heat transfer. Substitution into the boxed equation closes the model without an algebraic flash solve.

## Three formulations, three numerical properties

| Method | Two-phase thermodynamic unknowns | Main strength | Main cost or risk |
| --- | --- | --- | --- |
| Full-VLE-Algebraic | $\alpha_g,\rho_g,\rho_\ell,T$ | Direct, constraints solved to nonlinear tolerance | Four-variable nonlinear solve |
| Reduced-VLE-Algebraic | $T$ | Much cheaper while retaining algebraic enforcement | Depends on saturation correlations and still needs a scalar root solve |
| Reduced-VLE-ODE | $T$ as an evolved variable | No flash root solve; integrates naturally with explicit time stepping | Constraint and energy drift from time-discretization error |

The reduced algebraic method remains conservative because total energy is advanced by the conservation law and temperature is reconstructed from that energy. In the ODE method, temperature is advanced directly. A finite time step introduces truncation error in the equilibrium manifold, and reconstructing internal energy from the updated $(\rho,T)$ state exposes that error as energy drift.

This distinction matters. Two methods can give nearly indistinguishable pressure profiles over a short simulation while having different long-time conservation properties.

## Tank depressurization: seeing the thermodynamic path

In a tank blowdown, pressure and temperature initially fall through a single-phase region. When the saturation curve is reached, the trajectory follows it while vapour and liquid coexist. The process can then return to a single-phase gas as depressurization continues.

<figure class="research-figure">
  <img src="../../images/blog/reduced-vle/tank-trajectory.png" alt="Tank depressurization trajectory in pressure-temperature and density-energy spaces" loading="lazy" />
  <figcaption>The tank trajectory in $p$–$T$ and $\rho$–$e$ spaces. The saturation correlations make phase entry and exit geometrically explicit.</figcaption>
</figure>

All three formulations reproduce the benchmark tank pressure and temperature histories closely. The reduced algebraic approximation inherits the small uncertainty of the saturation correlations. The ODE formulation adds time-integration error, especially when a trajectory crosses a phase boundary where thermodynamic derivatives change non-smoothly.

## Accuracy versus computational cost

The reduced methods were approximately three to four times faster than the full four-variable flash in the studied cases. The algebraic and ODE reductions had comparable overall performance over much of the engineering-accuracy range.

<figure class="research-figure">
  <img src="../../images/blog/reduced-vle/TankErrorVsTimeTaken.png" alt="Relative temperature error plotted against CPU time for three equilibrium formulations" loading="lazy" />
  <figcaption>Temperature error versus CPU time. Reducing the thermodynamic problem shifts the accuracy–cost curve substantially.</figcaption>
</figure>

At tighter error targets, the ODE approach can lose some of its advantage because smaller time steps are needed near rapid phase transitions. This is a general lesson: removing a nonlinear solve does not remove stiffness or non-smooth thermodynamic behaviour; it changes where the computational difficulty appears.

## What happens to energy conservation?

For a conservative finite-volume method in a closed shock tube, the algebraic formulations preserve the discretized total energy up to solver and round-off errors. The ODE method evolves temperature with a first-order time integrator. Its local temperature error is $O(\Delta t^2)$, which accumulates over $O(1/\Delta t)$ steps into a global drift of approximately $O(\Delta t)$.

That does not make the ODE formulation unusable. It suggests a practical hybrid strategy:

1. use the ODE update when the state evolves smoothly;
2. monitor an energy or equilibrium residual;
3. reduce the time step near a phase crossing;
4. temporarily project back to the algebraic constraint if the residual exceeds a tolerance.

The algebraic formulation is the safer default when strict energy conservation is the priority. The ODE formulation is attractive when thermodynamic solves dominate cost and controlled drift is acceptable.

## Phase change reshapes the Riemann solution

The pipeline shock-tube test contains a left-going rarefaction, a contact discontinuity, and a right-going shock. The rarefaction begins in single-phase liquid and crosses the saturation boundary. At that crossing, the equilibrium sound speed falls from roughly $335\ \mathrm{m/s}$ to $55\ \mathrm{m/s}$ in the reported case.

<figure class="research-figure">
  <img src="../../images/blog/reduced-vle/ShockTube_AllVars_10000Cells.png" alt="Pressure, temperature, velocity, phase fraction, sound speed, and density profiles in a carbon-dioxide shock tube" loading="lazy" />
  <figcaption>The coupled flow and thermodynamic profiles. The plateau near the phase boundary appears simultaneously in pressure, temperature, and vapour fraction.</figcaption>
</figure>

Because a finite interval of characteristic speeds is skipped by the sound-speed jump, the rarefaction separates into a single-phase fan and a two-phase fan with a constant intermediate state.

<figure class="research-figure">
  <img src="../../images/blog/reduced-vle/RP_Characteristics_TwoPhase.png" alt="Characteristic diagram of a composite rarefaction, contact discontinuity, and shock" loading="lazy" />
  <figcaption>Characteristic structure of the composite rarefaction. The blank interval between the two fans corresponds to the constant plateau state.</figcaption>
</figure>

The same mechanism can be read in thermodynamic space. In the $p$–$T$ plane the expansion reaches the saturation line and follows it. In the $p$–$v$ plane the isentrope develops a kink at the phase boundary; since the isentropic slope determines sound speed, that kink explains the acoustic discontinuity.

<!-- <figure class="research-figure">
  <img src="../../images/blog/reduced-vle/thermodynamic-paths.png" alt="Pressure-temperature and pressure-volume trajectories through a phase transition" loading="lazy" />
  <figcaption>The same Riemann solution viewed in thermodynamic coordinates.</figcaption>
</figure> -->

<figure class="research-figure">
  <div class="figure-panel-grid">
    <div class="figure-panel">
      <img
        src="../../images/blog/reduced-vle/PTprofileWithRiemannWaves.png"
        alt="Riemann-wave solution in pressure-temperature space"
        loading="lazy"
      />
      <p><strong>(a)</strong> Pressure–temperature profile</p>
    </div>
    <div class="figure-panel">
      <img
        src="../../images/blog/reduced-vle/PVprofileWithRiemannWaves.png"
        alt="Riemann-wave solution in pressure-volume space"
        loading="lazy"
      />
      <p><strong>(b)</strong> Pressure–volume profile</p>
    </div>
  </div>

  <figcaption>
    Thermodynamic representation of the Riemann solution. The
    pressure–temperature trajectory reaches and follows the saturation curve,
    while the pressure–volume trajectory illustrates the change in isentropic
    behaviour across the phase boundary.
  </figcaption>
</figure>

## Validation beyond idealized shock tubes

The reduced algebraic method was also compared with large-scale CO₂ release experiments from the Dalian facility. The cases cover gaseous and dense initial states, several orifice sizes, and full-bore rupture. A finite-orifice outlet condition permits choked two-phase discharge.

The simulations capture the main depressurization time scales and trends. Deviations are most visible in the fastest rupture cases and can partly reflect physical effects excluded from the model, especially heat transfer between the fluid, pipe wall, and surroundings. Validation therefore does more than award a pass or fail: it shows which missing physics becomes important in which regime.

## Limits and the broader lesson

The reduction depends on accurate saturation relations and on the pure-component structure. It does not directly extend to CO₂-rich mixtures, where phase compositions vary independently. The ODE version also assumes enough regularity to differentiate the equilibrium relation, while phase boundaries introduce derivative discontinuities.

Nevertheless, the main idea generalizes: **choose thermodynamic variables and constraints to match the geometry of the physical problem**. For pure CO₂, the saturation curve turns a four-variable flash into one scalar relation. Differentiating that relation exposes an alternate dynamical formulation. The result is not merely a faster subroutine; it clarifies exactly where conservation, equilibrium, smoothness, and computational cost trade against one another.