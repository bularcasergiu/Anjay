/*
 * Copyright 2017 AVSystem <avsystem@avsystem.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <config.h>

#include "tx_params.h"

VISIBILITY_SOURCE_BEGIN

void _anjay_coap_update_retry_state(coap_retry_state_t *retry_state,
                                    const anjay_coap_tx_params_t *tx_params,
                                    anjay_rand_seed_t *rand_seed) {
    ++retry_state->retry_count;
    if (retry_state->retry_count == 1) {
        uint32_t delta = (uint32_t) (tx_params->ack_timeout_ms *
                (tx_params->ack_random_factor - 1.0));
        retry_state->recv_timeout_ms = tx_params->ack_timeout_ms +
                (int32_t) (_anjay_rand32(rand_seed) % delta);
    } else {
        retry_state->recv_timeout_ms *= 2;
    }
}
