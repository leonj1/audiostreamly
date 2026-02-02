import WorkOS from "@auth/core/providers/workos";
import { convexAuth } from "@convex-dev/auth/server";

export const { auth, signIn, signOut, store, isAuthenticated } = convexAuth({
  providers: [
    WorkOS({
      clientId: process.env.AUTH_WORKOS_CLIENT_ID,
      clientSecret: process.env.AUTH_WORKOS_CLIENT_SECRET,
      // WorkOS connection ID - configure this in WorkOS dashboard
      // Leave empty to use AuthKit (WorkOS's universal login)
      connection: process.env.AUTH_WORKOS_CONNECTION_ID,
    }),
  ],
});
