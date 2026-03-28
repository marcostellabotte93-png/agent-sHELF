# Go Code Review Guidelines

## Gestione degli errori

- Controlla sempre `if err != nil` dopo ogni chiamata che restituisce un errore — mai ignorare con `_` salvo casi espliciti e giustificati
- Usa `fmt.Errorf("operazione: %w", err)` per wrappare errori con contesto, mantenendo la chain per `errors.Is()` e `errors.As()`
- Usa `errors.Is()` per confrontare errori sentinel, `errors.As()` per estrarre tipi specifici
- Non tornare `nil, nil` da funzioni che possono fallire — è ambiguo per il chiamante

```go
// Problematico
func leggiFile(path string) ([]byte, error) {
    data, _ := os.ReadFile(path) // errore ignorato
    return data, nil
}

// Corretto
func leggiFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("leggiFile %s: %w", path, err)
    }
    return data, nil
}
```

## Concorrenza

- **Principio fondamentale**: non comunicare condividendo memoria — condividi memoria comunicando (channels)
- **Goroutine leak**: ogni goroutine avviata deve avere un percorso di uscita definito; evita goroutine avviate e mai terminate
- `context.Context` deve essere il primo parametro di qualsiasi funzione che esegue I/O o operazioni potenzialmente lente
- Usa `select` con `case <-ctx.Done()` per goroutine cancellabili
- `sync.WaitGroup` per attendere un gruppo di goroutine prima di proseguire
- `sync.Mutex` vs `sync.RWMutex`: preferisci `RWMutex` quando le letture superano di gran lunga le scritture
- Attenzione alle data race: usa `go test -race` nel CI

```go
// Goroutine con context e uscita definita
func worker(ctx context.Context, jobs <-chan Job) {
    for {
        select {
        case job, ok := <-jobs:
            if !ok {
                return // channel chiuso
            }
            process(job)
        case <-ctx.Done():
            return // cancellazione esterna
        }
    }
}
```

## Struttura del codice e naming

- Package naming: nomi brevi, singolari, minuscolo, senza underscore (es. `httputil`, non `http_util`)
- **Interfacce piccole**: "accept interfaces, return structs" — un'interfaccia con 1-2 metodi è preferibile a mega-interfacce
- Non esportare tipi, funzioni o variabili che non fanno parte dell'API pubblica del package
- Costruttori: funzioni `NewXxx()` per tipi che richiedono inizializzazione non banale
- Commenti esportati: ogni simbolo esportato deve avere un commento godoc che inizia con il nome del simbolo

## Performance

- Evita allocazioni inutili in hot path: riusa slice con `append` invece di creare nuovi slice
- String building in loop: usa `strings.Builder` invece di concatenazione con `+`
- Pre-alloca slice quando conosci la dimensione: `make([]T, 0, n)`
- Conversione `string` ↔ `[]byte` alloca — evita in loop critici; usa `unsafe` solo se profilation lo giustifica
- Profila prima di ottimizzare: usa `pprof`, `go test -bench`, `go tool trace`

## Testing

- Usa `t.Parallel()` per test che possono girare concorrentemente — riduce il tempo totale di CI
- Table-driven tests per coprire molti casi con poco boilerplate:
```go
tests := []struct {
    name  string
    input string
    want  string
}{
    {"caso nominale", "input", "atteso"},
    {"stringa vuota", "", ""},
}
for _, tc := range tests {
    t.Run(tc.name, func(t *testing.T) {
        t.Parallel()
        got := MiaFunzione(tc.input)
        if got != tc.want {
            t.Errorf("got %q, want %q", got, tc.want)
        }
    })
}
```
- Usa `cmp.Diff` (golang.org/x/exp/cmp) per confronti leggibili su struct complesse
- Separa integration test con build tag: `//go:build integration` e runnali esplicitamente con `-tags integration`
