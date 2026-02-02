"use client";

import { useAuthActions } from "@convex-dev/auth/react";
import { Authenticated, Unauthenticated, AuthLoading } from "convex/react";

export function AuthButton() {
  // Check if Convex is configured
  if (!process.env.NEXT_PUBLIC_CONVEX_URL) {
    return (
      <a
        href="#get-started"
        className="inline-flex items-center justify-center px-5 py-2.5 bg-primary hover:bg-primary-hover text-white font-medium rounded-lg transition-colors"
      >
        Get Started
      </a>
    );
  }

  return (
    <>
      <AuthLoading>
        <button
          disabled
          className="inline-flex items-center justify-center px-5 py-2.5 bg-gray-300 text-gray-500 font-medium rounded-lg cursor-not-allowed"
        >
          Loading...
        </button>
      </AuthLoading>
      <Authenticated>
        <SignOutButton />
      </Authenticated>
      <Unauthenticated>
        <SignInButton />
      </Unauthenticated>
    </>
  );
}

function SignInButton() {
  const { signIn } = useAuthActions();
  
  return (
    <button
      onClick={() => signIn("workos")}
      className="inline-flex items-center justify-center px-5 py-2.5 bg-primary hover:bg-primary-hover text-white font-medium rounded-lg transition-colors"
    >
      Sign In
    </button>
  );
}

function SignOutButton() {
  const { signOut } = useAuthActions();
  
  return (
    <button
      onClick={() => signOut()}
      className="inline-flex items-center justify-center px-5 py-2.5 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg transition-colors"
    >
      Sign Out
    </button>
  );
}

export function UserInfo() {
  if (!process.env.NEXT_PUBLIC_CONVEX_URL) {
    return null;
  }

  return (
    <>
      <AuthLoading>
        <span className="text-gray-400">Loading...</span>
      </AuthLoading>
      <Authenticated>
        <span className="text-gray-600">Signed in ✓</span>
      </Authenticated>
    </>
  );
}
