---
layout: ../layouts/MarkdownLayout.astro
title: Research
description: Numerical methods for phase equilibrium, multiphase flow, computational electromagnetics, and numerical relativity.
---

My research concerns the formulation and numerical solution of physical systems governed by hyperbolic partial differential equations, nonlinear constitutive models, and algebraic constraints. I am particularly interested in the point where mathematical formulation and numerical implementation meet: the choice of variables, governing equations, and constraints often determines whether a simulation is robust, efficient, and physically meaningful.

My current work focuses on thermodynamic phase equilibrium and CO₂-rich multiphase transport. I also work on finite-volume methods for Maxwell's equations and numerical formulations of Einstein's equations.

## Multiphase thermodynamics and phase equilibrium {#multiphase-thermodynamics}

Dynamic simulations of tanks, pipelines, and other closed or transient systems naturally evolve internal energy, volume, and material composition. Recovering pressure, temperature, phase amounts, and phase compositions from these quantities leads to the **UVN-flash problem**, in which total internal energy \(U\), volume \(V\), and component mole numbers \(\mathbf N\) are specified.

This problem is substantially more difficult than a conventional pressure–temperature flash. The algorithm must determine whether the mixture is thermodynamically stable as a single phase and, when it is unstable, calculate a stable multiphase equilibrium satisfying material, volume, energy, thermal, mechanical, and chemical-equilibrium conditions.

My work develops phase-equilibrium formulations that are compatible with Helmholtz-energy equations of state and suitable for repeated use inside dynamic simulations. The principal topics include:

- thermodynamic stability analysis and the detection of phase separation;
- generation of robust flash initial guesses from stability-analysis results;
- constrained entropy-maximisation formulations of the UVN-flash;
- reformulation of the problem in temperature–volume–composition variables;
- scaling, variable selection, derivatives, and nonlinear solution methods;
- efficient coupling between thermodynamic calculations and time-dependent flow solvers.

For pure CO₂, I reduced the conventional four-equation vapour–liquid-equilibrium system to a scalar nonlinear equation. I subsequently derived a temperature evolution equation directly from the equilibrium constraints. This permits temperature to be integrated together with the flow equations and can avoid repeatedly solving a complete nonlinear flash problem.

For multicomponent mixtures, I reformulated the UVN-flash in \(T\)-\(V\)-\(\mathbf N\) space as a constrained entropy-maximisation problem. The resulting formulation eliminates the nested temperature calculation required by traditional UVN-space approaches. It also provides a direct derivation of the associated thermodynamic Q-function and makes stability-derived initialisation part of the complete solution procedure.

Selected publications:

- [A new temperature evolution equation that enforces thermodynamic vapour–liquid equilibrium in multiphase flows — application to CO₂ modelling](https://doi.org/10.1016/j.compfluid.2024.106524)
- [Solving the UVN-flash problem in TVN-space](https://doi.org/10.1016/j.fluid.2025.114528)
- [A reformulation of UVN-flash for multicomponent two-phase systems with application to CO2-rich mixture transport in pipelines](https://doi.org/10.1016/j.compfluid.2026.107108)

## CO₂-rich multiphase transport {#co2-transport}

Carbon capture and storage requires the transport of large quantities of CO₂ from capture facilities to geological storage sites. Captured streams are not generally pure CO₂: impurities alter phase boundaries, density, speed of sound, decompression behaviour, and the temperatures reached during transient operations.

I develop numerical models that couple the fluid dynamics of CO₂-rich mixtures with thermodynamic stability and phase-equilibrium calculations. The flow is represented using the Homogeneous Equilibrium Model, while pressure and other thermodynamic quantities are obtained from a Helmholtz-energy equation of state.

In a finite-volume simulation, every computational cell must repeatedly answer three questions:

1. Is the current mixture stable as a single phase?
2. If not, what is the equilibrium phase split?
3. What pressure, temperature, phase fraction, and acoustic properties correspond to that equilibrium state?

My work treats these questions as part of the numerical flow model rather than delegating them to an isolated thermodynamic lookup. A tailored and better-scaled UVN-flash formulation is coupled to stability analysis and the finite-volume flow solver. The resulting framework has been applied to tank and pipeline depressurisation involving pure CO₂ and multicomponent CO₂-rich mixtures.

A current direction is the construction of thermodynamically consistent Riemann benchmarks for CO₂-rich flow. These reference solutions combine phase stability, UVN equilibrium, rarefaction and shock curves, and the multicomponent equilibrium speed of sound. Their purpose is to provide reproducible tests for approximate finite-volume pipeline solvers, particularly when a wave crosses a phase boundary.

Related publication:

- [A reformulation of UVN-flash for multicomponent two-phase systems with application to CO₂-rich mixture transport in pipelines](https://doi.org/10.1016/j.compfluid.2026.107108)

## Computational electromagnetics {#computational-electromagnetics}

My work in computational electromagnetics is based on the finite-volume time-domain method for Maxwell's equations. Maxwell's curl equations form a hyperbolic wave system, allowing ideas from computational fluid dynamics—characteristic decomposition, upwind fluxes, finite-volume balance laws, and explicit time integration—to be applied to electromagnetic propagation and scattering.

My master's research developed and assessed a characteristic FVTD solver in C++. The work progressed from one-dimensional wave propagation and material-interface problems to two-dimensional scattering on body-fitted meshes.

The one-dimensional studies included:

- perfect electric and perfect magnetic conductor boundaries;
- propagation through dielectric slabs;
- total-field and scattered-field formulations;
- absorbing outer-boundary conditions;
- first-order upwind and higher-order spatial schemes;
- numerical dispersion, dissipation, and accumulated phase error.

The two-dimensional studies considered transient scattering from perfectly conducting and dielectric circular cylinders using body-fitted O-grids. These calculations tested curved boundaries, electromagnetic polarisation, dielectric-interface fluxes, current extraction, mesh clustering, and delayed wave propagation.

A central conclusion of this work is that a numerically stable method is not necessarily sufficiently accurate for transient scattering. First-order upwinding reproduces the correct wave topology but can strongly attenuate weak or repeatedly reflected signals. Higher-order reconstruction is needed when phase accuracy, late-time behaviour, or small scattered fields are important.

My present interests include extending these ideas to three-dimensional and unstructured meshes, structure-preserving discretisations of Maxwell's equations, discrete divergence and curl compatibility, and efficient parallel implementations.

## Numerical relativity {#numerical-relativity}

Numerical relativity applies computational methods to Einstein's field equations. Unlike many standard evolution equations, the Einstein equations contain gauge freedom and differential constraints. A successful numerical method must therefore do more than approximate the continuum equations: it must control constraint violations, select appropriate gauge conditions, and provide a well-posed evolution system.

I am developing and comparing numerical implementations of several formulations:

- the Baumgarte–Shapiro–Shibata–Nakamura formulation;
- the conformal and covariant Z4 formulation;
- the first-order conformal and covariant Z4 formulation.

BSSN is a widely used second-order-in-space formulation. CCZ4 augments the conformal system with Z4 variables and constraint-damping terms. FO-CCZ4 introduces auxiliary gradient variables so that the complete evolution system is first order in space and time, making it particularly relevant to finite-volume, discontinuous-Galerkin, and high-resolution shock-capturing methods.

My current Julia implementations use BSSN and FO-CCZ4 to study:

- the relation between geometrical and evolved variables;
- gauge evolution and hyperbolicity;
- Hamiltonian, momentum, and reduction constraints;
- constraint damping and propagation;
- finite-difference and WENO spatial discretisations;
- explicit Runge–Kutta and strong-stability-preserving time integration;
- verification using standard numerical-relativity test problems.

The longer-term objective is a formulation-independent numerical framework in which BSSN, CCZ4, FO-CCZ4, Z4c, and related systems can share common infrastructure while retaining their distinct variables, derivative structure, and constraint equations.

## Numerical methods and scientific software {#scientific-software}

Across these research areas, software implementation is part of the scientific method. A numerical formulation is useful only when its assumptions, admissible states, convergence criteria, and failure modes are made explicit and tested.

My work combines:

- finite-volume and finite-difference discretisations;
- approximate and exact Riemann solvers;
- characteristic and high-resolution reconstruction;
- explicit Runge–Kutta time integration;
- Newton methods, line searches, and constrained optimisation;
- analytical and automatic differentiation;
- stability analysis and continuation methods;
- benchmark construction and convergence studies;
- parallel and performance-oriented scientific software.

I primarily use Julia, C++, and Python, together with MPI, multithreading, vectorisation, and GPU programming where appropriate. The emphasis is on reproducible solvers in which mathematical models, numerical algorithms, thermodynamic assumptions, and validation evidence remain visible.