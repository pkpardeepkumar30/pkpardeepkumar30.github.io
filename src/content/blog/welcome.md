---
title: "Why numerical reliability matters"
description: "A sample post showing the blog structure, Markdown authoring, and LaTeX support."
published: 2026-07-14
draft: true
tags:
  - numerical methods
  - scientific software
---

> This is a draft sample. Replace it with your own post and set `draft: false` when it is ready.

A numerical method is useful only when its assumptions, errors, and failure modes are understood. For a discrete approximation $u_h$ to a solution $u$, we often want a bound of the form

$$
\lVert u-u_h\rVert \leq C h^p,
$$

but convergence order is only one part of the story. Real scientific software must also handle difficult inputs, preserve physical constraints, and make its results reproducible.

This blog will collect plain-language explanations of those connections between mathematical analysis and implementation.
