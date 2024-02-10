1. Tricky to make logigng work - KEDRO_LOGGING_CONFIG
2. `logging.yml` settings is weird for plugins, it's not intuitively.
3. cli_hook_impl and hook_impl can actually used in a single plugin/hook.
4. Use DryRunner & hooks / resolve manually
5. DryRunner has bug `kedro.io.core.DatasetNotFoundError: Dataset 'dummy_1' not found in the catalog`
6. OmegaconfigLoader.__repr__ is missing some arguments