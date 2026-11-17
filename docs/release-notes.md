<!-- Describes the compiled RustRouter release and its supported platforms. -->
# RustRouter v0.3.0

- Includes the current weighted-routing locality, shared coordinate JNI, compact workspaces,
  bounded lower-bound preparation and adaptive coordinate-search improvements.
- Coordinate-search budgets can return feasible, non-optimal routes; flags expose truncation.
  Explicit-endpoint and stop-to-stop APIs remain exact. See docs/interop.md for policy settings.
- Windows x86-64 native libraries, Python wheel, Java clients and CLI are built and checked locally.
- Linux x86-64 JNI/C libraries are cross-compiled for glibc 2.17. Linux execution is not claimed.
- Native-only ZIPs support Maven without Rust/Cargo. Archives include source revision and checksums.
- Existing numeric JNI protocol 1 and client API 2 remain compatible.
- Hosted GitHub Actions currently fail before jobs start. These downloads are produced locally;
  this release does not claim new macOS binaries or successful hosted CI.

