/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import { ExtensibleFunction } from '../models';
import { isRequired } from '../utils';
import { NumberFormatFunction } from './types';
import {
  DEFALT_D3_FORMAT_PREFIXIES,
  FormatLocalePrefixies,
} from './D3FormatConfig';

export const PREVIEW_VALUE = 12345.432;

export interface NumberFormatterConfig {
  id: string;
  label?: string;
  description?: string;
  formatFunc: NumberFormatFunction;
  isInvalid?: boolean;
  prefixies?: FormatLocalePrefixies;
}

// Use type augmentation to indicate that
// an instance of NumberFormatter is also a function
interface NumberFormatter {
  (value: number | null | undefined): string;
}

class NumberFormatter extends ExtensibleFunction {
  id: string;

  label: string;

  description: string;

  formatFunc: NumberFormatFunction;

  isInvalid: boolean;

  prefixies: FormatLocalePrefixies;

  constructor(config: NumberFormatterConfig) {
    super((value: number) => this.format(value));

    const {
      id = isRequired('config.id'),
      label,
      description = '',
      formatFunc = isRequired('config.formatFunc'),
      isInvalid = false,
    } = config;
    this.id = id;
    this.label = label ?? id;
    this.description = description;
    this.formatFunc = formatFunc;
    this.isInvalid = isInvalid;
    this.prefixies = DEFALT_D3_FORMAT_PREFIXIES;
  }

  format(value: number | null | undefined) {
    if (value === null || value === undefined || Number.isNaN(value)) {
      return `${value}`;
    }
    if (value === Number.POSITIVE_INFINITY) {
      return '∞';
    }
    if (value === Number.NEGATIVE_INFINITY) {
      return '-∞';
    }

    let v = this.formatFunc(value);
    const char_position = v.search('[a-zA-Zµ]');
    if (char_position !== -1) {
      const p = v.charAt(char_position);
      const replace_value = this.prefixies[p];
      if (replace_value) {
        v = v.replace(p, ` ${replace_value}`);
      }
    }
    return v;
  }

  preview(value = PREVIEW_VALUE) {
    return `${value} => ${this.format(value)}`;
  }
}

export default NumberFormatter;
