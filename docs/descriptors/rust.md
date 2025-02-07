<!-- markdownlint-disable MD003 MD020 MD033 MD041 -->
<!-- @generated by .automation/build.py, please do not update manually -->
<!-- Instead, update descriptor file at https://github.com/nvuillam/mega-linter/tree/master/megalinter/descriptors/rust.yml -->
# RUST

## Linters

| Linter                   | Configuration key      |
|--------------------------|------------------------|
| [clippy](rust_clippy.md) | [RUST](rust_clippy.md) |

## Linted files

- File extensions:
  - `.rs`

## Configuration in Mega-Linter

| Variable                  | Description                   | Default value |
|---------------------------|-------------------------------|---------------|
| RUST_FILTER_REGEX_INCLUDE | Custom regex including filter |               |
| RUST_FILTER_REGEX_EXCLUDE | Custom regex excluding filter |               |


## Behind the scenes

### Installation

- Dockerfile commands :
```dockerfile
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
```

