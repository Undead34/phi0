import { Metadata } from "next";
import React, { Suspense } from "react";
import { DevtoolsProvider } from "@providers/devtools";
import { RefineKbarProvider } from "@refinedev/kbar"; // Command Bar CTRL + K

import "@styles/global.css";
import { Refine } from "@refinedev/core";
import { dataProvider } from "@providers/data-provider";

export const metadata: Metadata = {
  title: "Refine",
  description: "Generated by create refine app",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Suspense>
          <RefineKbarProvider>
            <DevtoolsProvider>
              <Refine dataProvider={dataProvider}>
                {children}
              </Refine>
            </DevtoolsProvider>
          </RefineKbarProvider>
        </Suspense>
      </body>
    </html>
  );
}
