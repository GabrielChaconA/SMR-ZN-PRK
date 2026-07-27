import type { LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"

interface StatCardProps {
  label: string
  value: number | string
  icon: LucideIcon
  accentClassName?: string
}

export function StatCard({ label, value, icon: Icon, accentClassName }: StatCardProps) {
  return (
    <div className="tech-card flex items-center gap-4 rounded-xl p-4 transition-transform hover:-translate-y-0.5">
      <div className={cn("flex size-12 shrink-0 items-center justify-center rounded-lg", accentClassName)}>
        <Icon className="size-6" aria-hidden="true" />
      </div>
      <div className="flex flex-col">
        <span className="text-sm text-muted-foreground">{label}</span>
        <span className="text-3xl font-semibold leading-tight text-card-foreground">{value}</span>
      </div>
    </div>
  )
}
