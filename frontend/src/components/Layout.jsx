// src/components/Layout.jsx
import { useState } from "react";
import Navbar from "./Navbar";
export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-base-200">
      <Navbar />

      <div className="flex">
        <main className="flex-1 p-4 md:p-8 overflow-x-hidden">{children}</main>
      </div>
    </div>
  );
}
