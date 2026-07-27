import { Car, CircleCheckBig, CircleSlash, Cpu, Radar } from "lucide-react"
import { StatCard } from "@/components/stat-card"

// Datos de ejemplo del estacionamiento
const TOTAL_SPOTS = 40

const spots = Array.from({ length: TOTAL_SPOTS }, (_, i) => {
  const row = String.fromCharCode(65 + Math.floor(i / 10)) // A, B, C, D
  const number = (i % 10) + 1
  // Ocupación de ejemplo
  const occupied = [0, 1, 3, 4, 7, 9, 11, 12, 15, 18, 21, 22, 23, 26, 29, 31, 34, 35, 38].includes(i)
  return { code: `${row}${number}`, occupied }
})

export default function Page() {
  const occupiedCount = spots.filter((s) => s.occupied).length
  const freeCount = TOTAL_SPOTS - occupiedCount
  const occupancy = Math.round((occupiedCount / TOTAL_SPOTS) * 100)

  return (
    <main className="tech-bg min-h-screen">
      <div className="mx-auto max-w-6xl px-4 py-8 md:px-6 lg:py-10">
        <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="glow-primary flex h-16 items-center justify-center rounded-2xl bg-white/95 px-2 ring-1 ring-primary/40">
              <img
                src="/images/smart-zone-park-logo.png"
                alt="Logo de Smart Zone Park"
                className="h-14 w-auto object-contain"
              />
            </div>
            <div>
              <h1 className="text-2xl font-semibold tracking-tight text-foreground text-balance text-glow">
                Smart Zone Park
              </h1>
              <p className="text-sm text-muted-foreground">Sistema de estacionamiento con IA</p>
            </div>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3 py-1.5">
            <span className="relative flex size-2">
              <span className="absolute inline-flex size-full animate-ping rounded-full bg-free opacity-75" />
              <span className="relative inline-flex size-2 rounded-full bg-free" />
            </span>
            <span className="text-xs font-medium text-foreground">Monitoreo en tiempo real</span>
          </div>
        </header>

        <div className="grid gap-6 md:grid-cols-[1fr_300px] lg:grid-cols-[1fr_320px]">
          {/* Vista del estacionamiento */}
          <section aria-label="Vista del estacionamiento" className="tech-card rounded-2xl p-4 md:p-6">
            <div className="mb-4 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Radar className="size-5 text-primary" aria-hidden="true" />
                <h2 className="text-lg font-medium text-card-foreground">Vista del estacionamiento</h2>
              </div>
              <span className="hidden items-center gap-1.5 rounded-md border border-primary/30 bg-primary/10 px-2 py-1 text-xs text-primary sm:flex">
                <Cpu className="size-3.5" aria-hidden="true" />
                Detección IA
              </span>
            </div>

            <div className="relative overflow-hidden rounded-xl ring-1 ring-primary/30">
              <img
                src="/images/parking-lot.png"
                alt="Vista aérea del estacionamiento con dos filas de autos estacionados en los espacios marcados"
                className="h-auto w-full object-cover"
              />
              {/* Superposición tecnológica sutil */}
              <div
                className="pointer-events-none absolute inset-0 mix-blend-screen"
                style={{
                  background:
                    "linear-gradient(180deg, oklch(0.62 0.19 258 / 0.18), transparent 30%, transparent 75%, oklch(0.17 0.04 258 / 0.5))",
                }}
                aria-hidden="true"
              />
              <div
                className="pointer-events-none absolute inset-0 opacity-30 mix-blend-overlay"
                style={{
                  backgroundImage:
                    "linear-gradient(oklch(0.7 0.15 250 / 0.5) 1px, transparent 1px), linear-gradient(90deg, oklch(0.7 0.15 250 / 0.5) 1px, transparent 1px)",
                  backgroundSize: "44px 44px",
                }}
                aria-hidden="true"
              />
            </div>
          </section>

          {/* Panel lateral de estadísticas */}
          <aside aria-label="Estadísticas" className="flex flex-col gap-4">
            <StatCard
              label="Total de carros"
              value={occupiedCount}
              icon={Car}
              accentClassName="bg-primary/15 text-primary ring-1 ring-primary/30"
            />
            <StatCard
              label="Espacios ocupados"
              value={occupiedCount}
              icon={CircleSlash}
              accentClassName="bg-occupied/15 text-occupied ring-1 ring-occupied/30"
            />
            <StatCard
              label="Espacios libres"
              value={freeCount}
              icon={CircleCheckBig}
              accentClassName="bg-free/15 text-free ring-1 ring-free/30"
            />

            <div className="tech-card mt-2 rounded-xl p-4">
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Ocupación</span>
                <span className="font-semibold text-card-foreground text-glow">{occupancy}%</span>
              </div>
              <div className="h-2.5 w-full overflow-hidden rounded-full bg-input">
                <div
                  className="glow-primary h-full rounded-full bg-primary transition-all"
                  style={{ width: `${occupancy}%` }}
                />
              </div>
              <p className="mt-3 text-xs text-muted-foreground">
                {occupiedCount} de {TOTAL_SPOTS} espacios ocupados
              </p>
            </div>
          </aside>
        </div>
      </div>
    </main>
  )
}
