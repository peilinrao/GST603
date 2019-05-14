.data					# section declaration

        # Useful offset constants for accessing members of a
        # struct mp1_blink_struct structure
        LOCATION   = 0
        ON_CHAR    = 2
        OFF_CHAR   = 3
        ON_LENGTH  = 4
        OFF_LENGTH = 6
        COUNTDOWN  = 8
        STATUS     = 10
        NEXT       = 12

        STRUCT_SIZE = 16

# Pointer to head of list (initialized to NULL)
mp1_list_head:
        .long   0

.text					# section declaration

# Export the function symbol names

.global mp1_rtc_tasklet
.global mp1_ioctl

# void mp1_poke(void);
#
# Interface: Register-based arguments (not C-style)
#    Inputs: %cl  - The byte you wish to write
#            %eax - Offset from the start of video memory that you wish
#                   to write to
#   Outputs: Text-mode video screen is written to at location %eax with
#            the byte in %cl
# Registers: Clobbers EDX
mp1_poke:

	movl    vmem_base_addr(,1),%edx
	movb    %cl,(%edx,%eax,1)
	ret

mp1_rtc_tasklet:
	ret

mp1_ioctl:
  movl  $1, %eax  #set return value to 1
  movl  8(%esp), %ebx  #load command number into ebx

  #check whether command number is valid
  cmpl  $3, %ebx
  jg invalid
  cmpl  $0, %ebx
  jl invalid

  #check jump_table to determine which function to call
  jmp *jump_table(, %ebx, 4)

  jmp mp1_ioctl_done


  #case command # is invalid
invalid:
  movl $-1, %eax  #set the return value to -1

  #calling procedure done, tear down the stack and return
mp1_ioctl_done:
	ret

mp1_ioctl_add:
  #callee save all regiters & update ebp
  pushl  %ebp
  movl  %esp, %ebp
  movl  8(%ebp), %esi

#malloc a structure
#  pushl  %eax
  #push 1 argument
  pushl  $STRUCT_SIZE
  call  mp1_malloc

  #tear down argument
  leal  4(%esp), %esp

  movl  %eax, %ebx   #use ebx to store the pointer
#  popl  %eax

#copy from user kernel
  #check null ptr
  cmpl  $0, %esi
  je  copy_error
#  pushl  %eax
  #push 3 arguments
  pushl  $STRUCT_SIZE
  pushl  %esi
  pushl  %ebx
  call  mp1_copy_from_user
  #tear down arguments
  leal  (%ebp), %esp

  #error detection
  cmpl  $0, %eax
  jne  copy_error

  #check location
        movw  LOCATION(%ebx), %cx
        cmpl  $0, %cx
  jl copy_error
        cmpl  $1999, %cx
  jg copy_error

  #adjust some parameters
        movw  ON_LENGTH(%ebx), %cx
        movw  %cx, COUNTDOWN(%ebx)
        movw  $1, STATUS(%ebx)

  #insert the structure
  movl  mp1_list_head, %ecx
  movl  %ecx, NEXT(%ebx)
  movl  %ebx, mp1_list_head

  #poke
  xorl  %ecx, %ecx
  movl  LOCATION(%ebx), %ecx
  leal  (%ecx, %ecx), %eax
  movb  ON_CHAR(%ebx), %cl
  call mp1_poke

  #set return value
  movl $0, %eax

#  popl  %eax
  jmp mp1_add_done

copy_error:
#free the memory
  pushl  %ebx
  call mp1_free
  movl 4(%esp), %esp

  movl  $-1, %eax

mp1_add_done:
  popl  %ebp
	ret

mp1_ioctl_remove:
	ret

mp1_ioctl_find:
	ret

mp1_ioctl_sync:
	ret


jump_table:
.long mp1_ioctl_add, mp1_ioctl_remove, mp1_ioctl_find, mp1_ioctl_sync


.end
