# Bottom Feeder Run Policy (Active)

> Venice Diem burn — 2026-04-09, 4:45 PM PT

```yaml
policy_id: bf-venice-diem-burn-2026-04-09
provider_lock: venice
allowed_models:
  - deepseek
  - qwen3-235b
  - glm-4.7
  - kimi-venice
  - llama3.3-venice
  - qwen3-next
  - oss-venice
duration_target_hours: 1
mode: burn
source_profile: all-optional-sources-enabled
stop_conditions:
  - venice balance < 0.50 Diem
  - all topics complete
  - explicit_user_stop
fallback_policy: if primary model 429s or errors, rotate to next allowed_model
checkpoint_interval_minutes: 15
```

## Budget

- Starting balance: ~5.09 Diem
- Reserve: 0.50 Diem (hard floor)
- Spendable: ~4.59 Diem

## Topic Queue (uncovered or stale)

Priority order:
1. **FHE-based private DeFi landscape** (Fhenix, Arcium, Zama) — no existing topic file
2. **Privacy L2 progress** (Namada, 0xMiden) — no existing topic file
3. **Swap aggregation architecture** (multi-DEX routing, MEV protection) — no existing topic file
4. **Supply chain attack protections** (npm/package ecosystems) — no existing topic file
5. **Secrets management for small teams** (Infisical, Vault, Doppler) — no existing topic file

## Enforcement Notes

- Use cheapest Venice models first (DeepSeek V3.2, Qwen3 235B, GLM 4.7, OSS-120B — all $0/Diem on Venice)
- Brave search as primary source, Perplexity as supplement for depth
- Write incrementally after each topic
- Stop gracefully when balance approaches reserve
