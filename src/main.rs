use wast::parser::{self, ParseBuffer};
use wast::Wat;
use std::fs;

fn main() {
    let wat:&str = r#"
    (module
      (type (;0;) (func (result i32)))
      (func $main (param $lhs i32) (param $rhs i32) (result i32)
        block (result i32)  ;; label = @1
          loop (result i32)  ;; label = @2
            local.get $lhs
            local.get $rhs
            br_if 0 (;@2;)
            br 1 (;@1;)
          end
        end
      )
      (export "main" (func $main))
    )    
    "#;
    let buf = ParseBuffer::new(wat).unwrap();
    let _ast = parser::parse::<wast::Wat>(&buf).unwrap();
    fs::write("./parsed_debug.txt", format!("{_ast:#?}")).expect("Unable to write file");
}
