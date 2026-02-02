import { httpRouter } from "convex/server";
import { auth } from "./auth";

const http = httpRouter();

// Add Convex Auth HTTP routes for OAuth callbacks
auth.addHttpRoutes(http);

export default http;
