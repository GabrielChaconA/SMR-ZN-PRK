import { Car } from "lucide-react"
import { cn } from "@/lib/utils"

interface ParkingSpotProps {
  code: string
  occupied: boolean
}

export function ParkingSpot({ code, occupied }: ParkingSpotProps) {
  return (
    <div
      className={cn(
        "relative flex aspect-square flex-col items-center justify-center gap-1 rounded-lg border-2 transition-colors",
        occupied
          ? "border-occupied/40 bg-occupied/10"
          : "border-dashed border-free/50 bg-free/10",
      )}
      role="img"
      aria-label={`Espacio ${code}: ${occupied ? "ocupado" : "libre"}`}
    >
      <span className="absolute left-1.5 top-1 text-[10px] font-medium text-muted-foreground">{code}</span>
      {occupied ? (
        <Car className="size-7 text-occupied" aria-hidden="true" />
      ) : (
        <span className="text-[11px] font-semibold uppercase tracking-wide text-free">Libre</span>
      )}
    </div>
  )
}
