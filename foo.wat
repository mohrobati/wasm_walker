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
