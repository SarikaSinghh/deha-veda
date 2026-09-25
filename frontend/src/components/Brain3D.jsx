import { Suspense, useEffect, useMemo, useRef, useState } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import {
  OrbitControls,
  Html,
  Environment,
  useGLTF,
} from "@react-three/drei";
import * as THREE from "three";
import {
  RotateCcw,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Info,
} from "lucide-react";

const MODEL_PATH = "/models/manas-brain.glb";

/*
 * The uploaded GLB contains four detailed anatomical meshes,
 * but they are generically named. We therefore use the model
 * primarily as the visual brain and create application-level
 * interactive regions around it.
 */

function BrainModel({ active, regions, onSelect }) {
  const group = useRef();
  const { scene } = useGLTF(MODEL_PATH);

  const clonedScene = useMemo(() => {
    const clone = scene.clone(true);

    clone.traverse((child) => {
      if (!child.isMesh) return;

      child.castShadow = true;
      child.receiveShadow = true;

      /*
       * Clone materials so changes do not mutate the cached GLB.
       */
      if (child.material) {
        child.material = child.material.clone();
        child.material.roughness = 0.72;
        child.material.metalness = 0.02;
      }
    });

    return clone;
  }, [scene]);

  /*
   * Normalize the imported model so it sits nicely inside
   * the viewer regardless of the original GLB dimensions.
   */
  useEffect(() => {
    if (!group.current) return;

    const box = new THREE.Box3().setFromObject(group.current);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());

    const largest = Math.max(size.x, size.y, size.z);

    if (largest > 0) {
      const scale = 3.15 / largest;
      group.current.scale.setScalar(scale);
    }

    group.current.position.set(
      -center.x * group.current.scale.x,
      -center.y * group.current.scale.y,
      -center.z * group.current.scale.z
    );
  }, [clonedScene]);

  /*
   * Very subtle breathing/presence animation.
   * It should feel alive without looking like a game object.
   */
  useFrame((state) => {
    if (!group.current) return;

    const target = active ? 1.015 : 1;

    const currentScale = group.current.userData.visualScale || 1;
    const nextScale = THREE.MathUtils.lerp(
      currentScale,
      target,
      0.06
    );

    group.current.userData.visualScale = nextScale;

    const baseScale = group.current.userData.baseScale || 1;
    group.current.scale.setScalar(baseScale * nextScale);

    /*
     * Very subtle floating movement.
     */
    group.current.position.y +=
      Math.sin(state.clock.elapsedTime * 0.7) * 0.0005;
  });

  return (
    <group ref={group}>
      <primitive object={clonedScene} />

      {regions.map((region, index) => (
        <BrainHotspot
          key={region.key || index}
          region={region}
          active={active?.key === region.key}
          onSelect={onSelect}
          index={index}
        />
      ))}
    </group>
  );
}

/*
 * Application-level anatomical hotspots.
 *
 * These are intentionally subtle. They allow the existing Manas
 * API regions to remain interactive even though the imported GLB
 * does not expose named anatomical meshes.
 */
function BrainHotspot({ region, active, onSelect, index }) {
  const ref = useRef();

  /*
   * Default positions are deliberately distributed around the
   * brain rather than pretending they are exact anatomical
   * coordinates.
   *
   * If the backend provides positions, those are preferred.
   */
  const position = useMemo(() => {
    if (
      Array.isArray(region.position) &&
      region.position.length === 3
    ) {
      return region.position;
    }

    const positions = [
      [0.55, 0.45, 0.72],
      [-0.55, 0.45, 0.72],
      [0.72, 0.02, 0.45],
      [-0.72, 0.02, 0.45],
      [0.35, -0.12, 0.82],
      [-0.35, -0.12, 0.82],
      [0.18, -0.58, 0.42],
      [-0.18, -0.58, 0.42],
    ];

    return positions[index % positions.length];
  }, [region.position, index]);

  useFrame((state) => {
    if (!ref.current) return;

    const pulse = active
      ? 1 + Math.sin(state.clock.elapsedTime * 3.2) * 0.08
      : 1;

    ref.current.scale.setScalar(pulse);
  });

  return (
    <group position={position}>
      <mesh
        ref={ref}
        onPointerOver={(event) => {
          event.stopPropagation();
          document.body.style.cursor = "pointer";
        }}
        onPointerOut={() => {
          document.body.style.cursor = "auto";
        }}
        onClick={(event) => {
          event.stopPropagation();
          onSelect(region);
        }}
      >
        <sphereGeometry args={[active ? 0.115 : 0.075, 24, 24]} />
        <meshStandardMaterial
          color={active ? "#0f766e" : "#5eead4"}
          emissive={active ? "#0f766e" : "#14b8a6"}
          emissiveIntensity={active ? 1.5 : 0.55}
          transparent
          opacity={active ? 0.95 : 0.55}
          roughness={0.25}
        />
      </mesh>

      {active && (
        <Html
          distanceFactor={7}
          position={[0.12, 0.12, 0]}
          center
          occlude
        >
          <div className="pointer-events-none whitespace-nowrap rounded-full border border-emerald-200 bg-white/95 px-3 py-1.5 text-[10px] font-semibold text-slate-800 shadow-lg backdrop-blur">
            {region.name}
          </div>
        </Html>
      )}
    </group>
  );
}

function BrainScene({ regions, active, onSelect, controlsRef }) {
  return (
    <>
      <ambientLight intensity={1.4} />

      <directionalLight
        position={[4, 6, 6]}
        intensity={2}
        castShadow
      />

      <directionalLight
        position={[-5, 2, 4]}
        intensity={0.8}
      />

      <directionalLight
        position={[0, -2, -5]}
        intensity={0.45}
      />

      <Environment preset="studio" />

      <BrainModel
        regions={regions}
        active={active}
        onSelect={onSelect}
      />

      <OrbitControls
        ref={controlsRef}
        enablePan={false}
        enableDamping
        dampingFactor={0.07}
        rotateSpeed={0.65}
        zoomSpeed={0.8}
        minDistance={3.2}
        maxDistance={7}
        minPolarAngle={0.35}
        maxPolarAngle={Math.PI - 0.35}
        target={[0, 0, 0]}
      />
    </>
  );
}

function LoadingBrain() {
  return (
    <div className="flex h-full items-center justify-center">
      <div className="text-center">
        <div className="mx-auto mb-4 h-10 w-10 animate-spin rounded-full border-2 border-slate-200 border-t-emerald-600" />
        <p className="font-data text-[10px] uppercase tracking-[0.22em] text-slate-500">
          Preparing anatomy
        </p>
      </div>
    </div>
  );
}

function WebGLFallback() {
  return (
    <div className="flex h-[520px] items-center justify-center rounded-[2rem] border border-slate-200 bg-[#F8F7F3] p-8 text-center">
      <div className="max-w-sm">
        <Info className="mx-auto mb-4 h-7 w-7 text-slate-400" />
        <h3 className="font-display text-xl font-semibold text-slate-900">
          Interactive anatomy unavailable
        </h3>
        <p className="mt-3 text-sm leading-relaxed text-slate-600">
          Your browser does not currently support the WebGL features
          required for the interactive brain model.
        </p>
      </div>
    </div>
  );
}

function hasWebGL() {
  try {
    const canvas = document.createElement("canvas");

    return Boolean(
      window.WebGLRenderingContext &&
        (canvas.getContext("webgl") ||
          canvas.getContext("experimental-webgl"))
    );
  } catch {
    return false;
  }
}

export function Brain3D({ regions = [], active, onSelect }) {
  const controlsRef = useRef(null);
  const [supported] = useState(hasWebGL);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [fullscreen, setFullscreen] = useState(false);

  const resetView = () => {
    const controls = controlsRef.current;

    if (!controls) return;

    controls.reset();
    controls.target.set(0, 0, 0);
    setZoomLevel(1);
  };

  const zoomIn = () => {
    const controls = controlsRef.current;

    if (!controls) return;

    const camera = controls.object;
    const direction = new THREE.Vector3();

    camera.getWorldDirection(direction);

    camera.position.addScaledVector(direction, 0.45);

    setZoomLevel((value) =>
      Math.min(2, Number((value + 0.12).toFixed(2)))
    );

    controls.update();
  };

  const zoomOut = () => {
    const controls = controlsRef.current;

    if (!controls) return;

    const camera = controls.object;
    const direction = new THREE.Vector3();

    camera.getWorldDirection(direction);

    camera.position.addScaledVector(direction, -0.45);

    setZoomLevel((value) =>
      Math.max(0.6, Number((value - 0.12).toFixed(2)))
    );

    controls.update();
  };

  const toggleFullscreen = () => {
    setFullscreen((value) => !value);
  };

  if (!supported) {
    return <WebGLFallback />;
  }

  return (
    <div
      className={`relative ${
        fullscreen
          ? "fixed inset-4 z-[100] h-[calc(100vh-2rem)]"
          : ""
      }`}
    >
      <div
        data-testid="brain-3d-canvas"
        className={`relative overflow-hidden rounded-[2rem] border border-slate-200 bg-[#F8F7F3] shadow-[0_20px_70px_rgba(15,23,42,0.08)] ${
          fullscreen ? "h-full" : "h-[520px]"
        }`}
      >
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_45%,rgba(255,255,255,0.95),rgba(248,247,243,0.25)_52%,rgba(241,240,235,0.7))]" />

        <Suspense fallback={<LoadingBrain />}>
          <Canvas
            camera={{
              position: [0, 0, 5],
              fov: 38,
              near: 0.1,
              far: 100,
            }}
            dpr={[1, 1.75]}
            shadows
            gl={{
              antialias: true,
              alpha: true,
              powerPreference: "high-performance",
            }}
          >
            <BrainScene
              regions={regions}
              active={active}
              onSelect={onSelect}
              controlsRef={controlsRef}
            />
          </Canvas>
        </Suspense>

        {/* Top-left identity */}
        <div className="pointer-events-none absolute left-5 top-5">
          <div className="rounded-2xl border border-white/80 bg-white/80 px-4 py-3 shadow-sm backdrop-blur-md">
            <p className="font-data text-[9px] uppercase tracking-[0.25em] text-emerald-700">
              Manas
            </p>
            <p className="mt-1 font-display text-sm font-semibold text-slate-900">
              Interactive Brain
            </p>
          </div>
        </div>

        {/* Controls */}
        <div className="absolute right-5 top-5 flex flex-col gap-2">
          <button
            data-testid="brain-zoom-in"
            type="button"
            aria-label="Zoom in"
            onClick={zoomIn}
            className="rounded-full border border-slate-200 bg-white/95 p-2.5 text-slate-700 shadow-sm transition hover:border-emerald-300 hover:text-emerald-700"
          >
            <ZoomIn className="h-4 w-4" />
          </button>

          <button
            data-testid="brain-zoom-out"
            type="button"
            aria-label="Zoom out"
            onClick={zoomOut}
            className="rounded-full border border-slate-200 bg-white/95 p-2.5 text-slate-700 shadow-sm transition hover:border-emerald-300 hover:text-emerald-700"
          >
            <ZoomOut className="h-4 w-4" />
          </button>

          <button
            data-testid="brain-reset-view"
            type="button"
            aria-label="Reset brain view"
            onClick={resetView}
            className="rounded-full border border-slate-200 bg-white/95 p-2.5 text-slate-700 shadow-sm transition hover:border-emerald-300 hover:text-emerald-700"
          >
            <RotateCcw className="h-4 w-4" />
          </button>

          <button
            type="button"
            aria-label={
              fullscreen
                ? "Exit fullscreen brain view"
                : "Open fullscreen brain view"
            }
            onClick={toggleFullscreen}
            className="rounded-full border border-slate-200 bg-white/95 p-2.5 text-slate-700 shadow-sm transition hover:border-emerald-300 hover:text-emerald-700"
          >
            <Maximize2 className="h-4 w-4" />
          </button>
        </div>

        {/* Bottom instruction */}
        <div className="pointer-events-none absolute bottom-5 left-1/2 -translate-x-1/2">
          <div className="whitespace-nowrap rounded-full border border-white/80 bg-white/80 px-4 py-2 shadow-sm backdrop-blur-md">
            <p className="font-data text-[9px] uppercase tracking-[0.18em] text-slate-500">
              Drag to rotate · Scroll to zoom · Select a region
            </p>
          </div>
        </div>

        {/* Active region indicator */}
        {active && (
          <div className="absolute bottom-5 right-5 hidden max-w-[220px] rounded-2xl border border-emerald-100 bg-white/90 p-4 shadow-sm backdrop-blur-md sm:block">
            <p className="font-data text-[9px] uppercase tracking-[0.18em] text-emerald-700">
              Selected
            </p>

            <p className="mt-1 font-display text-sm font-semibold text-slate-900">
              {active.name}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

useGLTF.preload(MODEL_PATH);