'use strict';

const { Schema, model } = require('mongoose');

const DealershipSchema = new Schema(
  {
    id: {
      type: Number,
      required: true,
      unique: true, // 既然用自增/手动 id，就防重复
    },
    city: {
      type: String,
      required: true,
      trim: true,
    },
    state: {
      type: String,
      required: true,
      trim: true,
      uppercase: true, // 例如 'CA'、'NY'；若不需要可去掉
    },
    address: {
      type: String,
      required: true,
      trim: true,
    },
    zip: {
      type: String,
      required: true,
      trim: true,
      uppercase: true, // 兼容美/加邮编；如只做美国，可加正则校验
      // match: [/^\d{5}(-\d{4})?$/, 'Invalid US ZIP'] 
    },
    // 用数字更合适，并加范围校验
    lat: {
      type: Number,
      required: true,
      min: -90,
      max: 90,
    },
    long: {
      type: Number,
      required: true,
      min: -180,
      max: 180,
    },
    short_name: {
      type: String,
      trim: true,
    },
    full_name: {
      type: String,
      required: true,
      trim: true,
    },
  },
  { timestamps: true }
);

// 常用查询的辅助索引（可选）
DealershipSchema.index({ state: 1, city: 1 });
DealershipSchema.index({ id: 1 }, { unique: true });

module.exports = model('Dealership', DealershipSchema);
