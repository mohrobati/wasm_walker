(module
  (type (;0;) (func))
  (type (;1;) (func (param i32 i32) (result i32)))
  (type (;2;) (func (param i32) (result i32)))
  (type (;3;) (func (param i32)))
  (import "env" "__linear_memory" (memory (;0;) 1))
  (import "env" "ATS_2d0_2e2_2e11_2src_2ats_array_2esats__staload" (func (;0;) (type 0)))
  (import "env" "ats_malloc_gc" (func (;1;) (type 2)))
  (import "env" "ats_free_gc" (func (;2;) (type 3)))
  (import "env" "__stack_pointer" (global (;0;) (mut i32)))
  (func $ATS_2d0_2e2_2e11_2src_2ats_array_2edats__staload (type 0)
    block  ;; label = @1
      i32.const 0
      i32.load8_u
      br_if 0 (;@1;)
      i32.const 0
      i32.const 1
      i32.store8
      call 0
    end)
  (func $ATS_2d0_2e2_2e11_2src_2ats_array_2edats__dynload (type 0)
    i32.const 0
    i32.const 1
    i32.store
    block  ;; label = @1
      i32.const 0
      i32.load8_u
      br_if 0 (;@1;)
      i32.const 0
      i32.const 1
      i32.store8
      call 0
    end)
  (func $ats_array_ptr_alloc_tsz (type 1) (param i32 i32) (result i32)
    local.get 1
    local.get 0
    i32.mul
    call 1)
  (func $ats_array_ptr_free (type 3) (param i32)
    local.get 0
    call 2)
  (data $ATS_2d0_2e2_2e11_2src_2ats_array_2edats__staload.ATS_2d0_2e2_2e11_2src_2ats_array_2edats__staload_flag (i32.const 0) "\00"))
