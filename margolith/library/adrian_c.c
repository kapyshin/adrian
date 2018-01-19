#include <stdint.h>
#include <stdlib.h>
#include <adrian_c.h>


IntFast8* IntFast8___init__(int_fast8_t literal) {
    IntFast8* self = malloc(sizeof(IntFast8));
    self->literal = literal;
    return self;
}

void IntFast8___deinit__(IntFast8* self) {
    free(self);
}

IntFast8* IntFast8___copy__(IntFast8* self) {
    IntFast8* new = malloc(sizeof(IntFast8));
    new->literal = self->literal;
    return new;
}

IntFast8* IntFast8___add__(IntFast8* self, IntFast8* src) {
    IntFast8* new = malloc(sizeof(IntFast8));
    new->literal = self->literal + src->literal;
    return new;
}

IntFast8* IntFast8___sub__(IntFast8* self, IntFast8* src) {
    IntFast8* new = malloc(sizeof(IntFast8));
    new->literal = self->literal - src->literal;
    return new;
}

IntFast8* IntFast8___mul__(IntFast8* self, IntFast8* src) {
    IntFast8* new = malloc(sizeof(IntFast8));
    new->literal = self->literal * src->literal;
    return new;
}

IntFast8* IntFast8___div__(IntFast8* self, IntFast8* src) {
    IntFast8* new = malloc(sizeof(IntFast8));
    new->literal = self->literal / src->literal;
    return new;
}

IntFast16* IntFast16___init__(int_fast16_t literal) {
    IntFast16* self = malloc(sizeof(IntFast16));
    self->literal = literal;
    return self;
}

void IntFast16___deinit__(IntFast16* self) {
    free(self);
}

IntFast16* IntFast16___copy__(IntFast16* self) {
    IntFast16* new = malloc(sizeof(IntFast16));
    new->literal = self->literal;
    return new;
}

IntFast16* IntFast16___add__(IntFast16* self, IntFast16* src) {
    IntFast16* new = malloc(sizeof(IntFast16));
    new->literal = self->literal + src->literal;
    return new;
}

IntFast16* IntFast16___sub__(IntFast16* self, IntFast16* src) {
    IntFast16* new = malloc(sizeof(IntFast16));
    new->literal = self->literal - src->literal;
    return new;
}

IntFast16* IntFast16___mul__(IntFast16* self, IntFast16* src) {
    IntFast16* new = malloc(sizeof(IntFast16));
    new->literal = self->literal * src->literal;
    return new;
}

IntFast16* IntFast16___div__(IntFast16* self, IntFast16* src) {
    IntFast16* new = malloc(sizeof(IntFast16));
    new->literal = self->literal / src->literal;
    return new;
}

IntFast32* IntFast32___init__(int_fast32_t literal) {
    IntFast32* self = malloc(sizeof(IntFast32));
    self->literal = literal;
    return self;
}

void IntFast32___deinit__(IntFast32* self) {
    free(self);
}

IntFast32* IntFast32___copy__(IntFast32* self) {
    IntFast32* new = malloc(sizeof(IntFast32));
    new->literal = self->literal;
    return new;
}

IntFast32* IntFast32___add__(IntFast32* self, IntFast32* src) {
    IntFast32* new = malloc(sizeof(IntFast32));
    new->literal = self->literal + src->literal;
    return new;
}

IntFast32* IntFast32___sub__(IntFast32* self, IntFast32* src) {
    IntFast32* new = malloc(sizeof(IntFast32));
    new->literal = self->literal - src->literal;
    return new;
}

IntFast32* IntFast32___mul__(IntFast32* self, IntFast32* src) {
    IntFast32* new = malloc(sizeof(IntFast32));
    new->literal = self->literal * src->literal;
    return new;
}

IntFast32* IntFast32___div__(IntFast32* self, IntFast32* src) {
    IntFast32* new = malloc(sizeof(IntFast32));
    new->literal = self->literal / src->literal;
    return new;
}

IntFast64* IntFast64___init__(int_fast64_t literal) {
    IntFast64* self = malloc(sizeof(IntFast64));
    self->literal = literal;
    return self;
}

void IntFast64___deinit__(IntFast64* self) {
    free(self);
}

IntFast64* IntFast64___copy__(IntFast64* self) {
    IntFast64* new = malloc(sizeof(IntFast64));
    new->literal = self->literal;
    return new;
}

IntFast64* IntFast64___add__(IntFast64* self, IntFast64* src) {
    IntFast64* new = malloc(sizeof(IntFast64));
    new->literal = self->literal + src->literal;
    return new;
}

IntFast64* IntFast64___sub__(IntFast64* self, IntFast64* src) {
    IntFast64* new = malloc(sizeof(IntFast64));
    new->literal = self->literal - src->literal;
    return new;
}

IntFast64* IntFast64___mul__(IntFast64* self, IntFast64* src) {
    IntFast64* new = malloc(sizeof(IntFast64));
    new->literal = self->literal * src->literal;
    return new;
}

IntFast64* IntFast64___div__(IntFast64* self, IntFast64* src) {
    IntFast64* new = malloc(sizeof(IntFast64));
    new->literal = self->literal / src->literal;
    return new;
}

UIntFast8* UIntFast8___init__(uint_fast8_t literal) {
    UIntFast8* self = malloc(sizeof(UIntFast8));
    self->literal = literal;
    return self;
}

void UIntFast8___deinit__(UIntFast8* self) {
    free(self);
}

UIntFast8* UIntFast8___copy__(UIntFast8* self) {
    UIntFast8* new = malloc(sizeof(UIntFast8));
    new->literal = self->literal;
    return new;
}

UIntFast8* UIntFast8___add__(UIntFast8* self, UIntFast8* src) {
    UIntFast8* new = malloc(sizeof(UIntFast8));
    new->literal = self->literal + src->literal;
    return new;
}

UIntFast8* UIntFast8___sub__(UIntFast8* self, UIntFast8* src) {
    UIntFast8* new = malloc(sizeof(UIntFast8));
    new->literal = self->literal - src->literal;
    return new;
}

UIntFast8* UIntFast8___mul__(UIntFast8* self, UIntFast8* src) {
    UIntFast8* new = malloc(sizeof(UIntFast8));
    new->literal = self->literal * src->literal;
    return new;
}

UIntFast8* UIntFast8___div__(UIntFast8* self, UIntFast8* src) {
    UIntFast8* new = malloc(sizeof(UIntFast8));
    new->literal = self->literal / src->literal;
    return new;
}

UIntFast16* UIntFast16___init__(uint_fast16_t literal) {
    UIntFast16* self = malloc(sizeof(UIntFast16));
    self->literal = literal;
    return self;
}

void UIntFast16___deinit__(UIntFast16* self) {
    free(self);
}

UIntFast16* UIntFast16___copy__(UIntFast16* self) {
    UIntFast16* new = malloc(sizeof(UIntFast16));
    new->literal = self->literal;
    return new;
}

UIntFast16* UIntFast16___add__(UIntFast16* self, UIntFast16* src) {
    UIntFast16* new = malloc(sizeof(UIntFast16));
    new->literal = self->literal + src->literal;
    return new;
}

UIntFast16* UIntFast16___sub__(UIntFast16* self, UIntFast16* src) {
    UIntFast16* new = malloc(sizeof(UIntFast16));
    new->literal = self->literal - src->literal;
    return new;
}

UIntFast16* UIntFast16___mul__(UIntFast16* self, UIntFast16* src) {
    UIntFast16* new = malloc(sizeof(UIntFast16));
    new->literal = self->literal * src->literal;
    return new;
}

UIntFast16* UIntFast16___div__(UIntFast16* self, UIntFast16* src) {
    UIntFast16* new = malloc(sizeof(UIntFast16));
    new->literal = self->literal / src->literal;
    return new;
}

UIntFast32* UIntFast32___init__(uint_fast32_t literal) {
    UIntFast32* self = malloc(sizeof(UIntFast32));
    self->literal = literal;
    return self;
}

void UIntFast32___deinit__(UIntFast32* self) {
    free(self);
}

UIntFast32* UIntFast32___copy__(UIntFast32* self) {
    UIntFast32* new = malloc(sizeof(UIntFast32));
    new->literal = self->literal;
    return new;
}

UIntFast32* UIntFast32___add__(UIntFast32* self, UIntFast32* src) {
    UIntFast32* new = malloc(sizeof(UIntFast32));
    new->literal = self->literal + src->literal;
    return new;
}

UIntFast32* UIntFast32___sub__(UIntFast32* self, UIntFast32* src) {
    UIntFast32* new = malloc(sizeof(UIntFast32));
    new->literal = self->literal - src->literal;
    return new;
}

UIntFast32* UIntFast32___mul__(UIntFast32* self, UIntFast32* src) {
    UIntFast32* new = malloc(sizeof(UIntFast32));
    new->literal = self->literal * src->literal;
    return new;
}

UIntFast32* UIntFast32___div__(UIntFast32* self, UIntFast32* src) {
    UIntFast32* new = malloc(sizeof(UIntFast32));
    new->literal = self->literal / src->literal;
    return new;
}

UIntFast64* UIntFast64___init__(uint_fast64_t literal) {
    UIntFast64* self = malloc(sizeof(UIntFast64));
    self->literal = literal;
    return self;
}

void UIntFast64___deinit__(UIntFast64* self) {
    free(self);
}

UIntFast64* UIntFast64___copy__(UIntFast64* self) {
    UIntFast64* new = malloc(sizeof(UIntFast64));
    new->literal = self->literal;
    return new;
}

UIntFast64* UIntFast64___add__(UIntFast64* self, UIntFast64* src) {
    UIntFast64* new = malloc(sizeof(UIntFast64));
    new->literal = self->literal + src->literal;
    return new;
}

UIntFast64* UIntFast64___sub__(UIntFast64* self, UIntFast64* src) {
    UIntFast64* new = malloc(sizeof(UIntFast64));
    new->literal = self->literal - src->literal;
    return new;
}

UIntFast64* UIntFast64___mul__(UIntFast64* self, UIntFast64* src) {
    UIntFast64* new = malloc(sizeof(UIntFast64));
    new->literal = self->literal * src->literal;
    return new;
}

UIntFast64* UIntFast64___div__(UIntFast64* self, UIntFast64* src) {
    UIntFast64* new = malloc(sizeof(UIntFast64));
    new->literal = self->literal / src->literal;
    return new;
}