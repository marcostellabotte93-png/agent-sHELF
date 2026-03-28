# Guida alle Metriche Aziendali

Questa skill definisce le metriche chiave dell'azienda, la loro logica di calcolo e i reference per trovarle in Looker. Usala come fonte di verità quando una metrica è ambigua o l'utente chiede come viene calcolata.

## Metriche Revenue

### MRR (Monthly Recurring Revenue)
- **Definizione**: fatturato ricorrente mensile generato da contratti attivi
- **Esclude**: revenue one-time, contratti in stato `churned`, `paused`, `trial`
- **Looker**: Explore `subscriptions` → misura `subscriptions.mrr`
- **Attenzione**: il MRR si misura sempre all'ultimo giorno del mese (snapshot di fine mese)

### ARR (Annual Recurring Revenue)
- **Definizione**: MRR × 12 — proiezione annua del ricorrente corrente
- **Looker**: Explore `subscriptions` → misura `subscriptions.arr`

### Net Revenue Retention (NRR)
- **Definizione**: quanto revenue viene mantenuta e espansa dalla base clienti esistente
- **Formula**: `(MRR fine periodo - MRR new business) / MRR inizio periodo × 100`
- **Target benchmark SaaS**: NRR > 100% indica espansione netta

### Churn Rate (Revenue Churn)
- **Definizione**: percentuale di MRR persa nel periodo per cancellazioni e downsell
- **Formula**: `MRR churned nel periodo / MRR inizio periodo × 100`
- **Looker**: Explore `subscriptions` → misura `subscriptions.revenue_churn_rate`
- **Distinto da**: Logo Churn (% clienti), che è una metrica separata

## Metriche Prodotto

### DAU / MAU (Daily / Monthly Active Users)
- **Definizione**: utenti unici con almeno una sessione nel giorno / mese
- **Looker**: Explore `events` → filtra `event_type = 'session_start'` → misura `events.unique_users`
- **DAU/MAU Ratio**: indicatore di stickiness — target: > 20% per prodotti B2B, > 40% per consumer

### Feature Adoption Rate
- **Definizione**: % di utenti attivi del periodo che hanno usato una feature specifica almeno una volta
- **Formula**: `utenti_che_hanno_usato_feature / MAU × 100`
- **Looker**: Explore `events` → filtra su `feature_name` → misura `events.unique_users` / `users.mau`

### Time to Value (TTV)
- **Definizione**: tempo mediano tra primo login e completamento del primo "momento valueat" (definito per product area)
- **Looker**: Explore `user_journeys` → misura `user_journeys.median_ttv_days`

## Metriche Cliente

### NPS (Net Promoter Score)
- **Range**: da -100 a +100
- **Calcolo**: `% Promotori (voto 9-10) − % Detrattori (voto 0-6)`, i Passivi (7-8) non contano
- **Looker**: Explore `surveys` → misura `surveys.nps_score`
- **Frequenza raccolta**: trimestrale per clienti Enterprise, in-app mensile per SMB

### CSAT (Customer Satisfaction Score)
- **Definizione**: % risposte positive (4-5 su scala 1-5) su survey post-interazione
- **Formula**: `risposte_positive / totale_risposte × 100`

### CAC (Customer Acquisition Cost)
- **Definizione**: costo totale di marketing + vendite diviso per i nuovi clienti acquisiti nel periodo
- **Formula**: `(spesa_marketing + spesa_sales) / nuovi_clienti_periodo`
- **Distingui**: CAC blended (tutte le sorgenti) vs CAC per canale

### LTV (Lifetime Value)
- **Definizione semplificata**: ARPU × durata media contratto in mesi
- **Definizione avanzata**: somma del MRR atteso per tutta la durata del contratto, scontata
- **Ratio LTV:CAC target**: > 3x per business SaaS sano

## Note sull'interpretazione

- **Periodi parziali**: metriche del mese in corso appaiono inferiori per definizione — normalizza sempre o confronta MTD vs MTD anno precedente
- **Cambi di definizione**: variazioni brusche di una metrica possono indicare un cambio di tracciamento, non un cambio reale — verifica con il team Data
- **Segmentazione**: le metriche aggregate nascondono dinamiche importanti — segmenta sempre per piano, industria, cohort quando possibile
