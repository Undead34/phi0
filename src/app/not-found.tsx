"use client";

import { Suspense } from "react";
import { ErrorComponent } from "@refinedev/core";

export default function NotFound() {
  return (
    <Suspense>
      <ErrorComponent />
    </Suspense>
  );
}
